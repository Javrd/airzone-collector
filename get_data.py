import yaml
from time import time

import requests
from influxdb import InfluxDBClient

client = InfluxDBClient(host='localhost', port=8086)


class AirZoneAPI():
    BASE_URL = 'https://m.airzonecloud.com/api/v1'
    MODES = {
        "0": "Stop",
        "1": "Auto",
        "2": "Cooling",
        "3": "Heating",
        "4": "Ventilation",
        "5": "Dehumidifier/Dry",
        "6": "Emergency Heat",
        "7": "Heat air",
        "8": "Heat radiant",
        "9": "Heat combined",
        "10": "Cooling air",
        "11": "Cooling radiant",
        "12": "Cooling combined"
    }

    def __init__(self):
        with open('/home/javrd/sensorhome/.settings.yaml', 'r') as f:
            settings: dict = yaml.safe_load(f)

        token = settings.get('token', '')
        self.refresh_token = settings.get('refresh_token', '')
        self.installation_id = settings.get('installation_id', '')
        self.devices = settings.get('devices', {})
        self.headers = {'Authorization': f'Bearer {token}'}

        if not self.installation_id:
            self.installation_id = self.get_installation_id()

        if not self.devices:
            self.devices = self.get_devices()

    @staticmethod
    def update_settings(field, value):
        with open('/home/javrd/sensorhome/.settings.yaml', 'r') as f:
            settings = yaml.safe_load(f)
        if not settings:
            settings = {}
        settings[field] = value
        with open('/home/javrd/sensorhome/.settings.yaml', 'w') as f:
            yaml.dump(settings,
                      f,
                      default_flow_style=False,
                      allow_unicode=True)

    def request_refresh_token(self):
        auth_response = requests.get(
            f'{self.BASE_URL}/auth/refreshToken/{self.refresh_token}')
        auth_response.raise_for_status()
        auth_json = auth_response.json()
        AirZoneAPI.update_settings('token', auth_json['token'])
        AirZoneAPI.update_settings('refresh_token', auth_json['refreshToken'])
        self.headers = {'Authorization': f'Bearer {auth_json["token"]}'}

    def get_installation_id(self):
        installations = requests.get(f'{self.BASE_URL}/installations',
                                     headers=self.headers)
        if installations.status_code in [401, 403]:
            self.request_refresh_token()
            installations = requests.get(f'{self.BASE_URL}/installations',
                                         headers=self.headers)
        installations.raise_for_status()
        installations_json = installations.json()
        installation_id = installations_json['installations'][0][
            'installation_id']
        AirZoneAPI.update_settings('installation_id', installation_id)

        return installation_id

    def get_devices(self):
        devices_request = requests.get(
            f'{self.BASE_URL}/installations/{self.installation_id}',
            headers=self.headers)
        if devices_request.status_code in [401, 403]:
            self.request_refresh_token()
            devices_request = requests.get(
                f'{self.BASE_URL}/installations/{self.installation_id}',
                headers=self.headers)
        devices_request.raise_for_status()
        devices_json = devices_request.json()
        devices = {
            device['name']: device['device_id']
            for device in devices_json['groups'][0]['devices']
            if 'name' in device.keys()
        }
        AirZoneAPI.update_settings('devices', devices)

        return devices

    def get_device_status(self, device_id):
        status_response = requests.get(
            f'{self.BASE_URL}/devices/{device_id}/status',
            params={'installation_id': self.installation_id},
            headers=self.headers)
        if status_response.status_code in [401, 403]:
            self.request_refresh_token()
            status_response = requests.get(
                f'{self.BASE_URL}/devices/{device_id}/status',
                params={'installation_id': self.installation_id},
                headers=self.headers)
        status_response.raise_for_status()

        return status_response.json()


if __name__ == '__main__':
    airzone_client = AirZoneAPI()

    timestamp = round(time() * 1000)
    data = []
    for device_name, device_id in airzone_client.devices.items():
        status_json = airzone_client.get_device_status(device_id)
        data.append({
            "measurement": "temperature",
            "tags": {
                "location": device_name,
                "mode": airzone_client.MODES[str(status_json["mode"])],
                "power": status_json["power"]
            },
            "fields": {
                "value": float(status_json["local_temp"]["celsius"]),
            },
            "time": timestamp
        })

        data.append({
            "measurement": "humidity",
            "tags": {
                "location": device_name,
                "mode": airzone_client.MODES[str(status_json["mode"])],
                "power": status_json["power"]
            },
            "fields": {
                "value": status_json["humidity"]
            },
            "time": timestamp
        })

    client.write_points(data,
                        database='sensorhome',
                        time_precision='ms',
                        batch_size=10000,
                        protocol='json')
