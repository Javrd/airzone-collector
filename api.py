import os
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
import yaml

from utils import cwd, update_settings


class AirZoneAPI():
    BASE_URL = 'https://m.airzonecloud.com/api/v1'

    def __init__(self):

        with open(os.path.join(cwd, '.settings.yaml'), 'r') as f:
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

    def retry_on_auth_error(func):
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except requests.HTTPError as error:
                if error.response.status_code in [401, 403]:
                    self.request_refresh_token()
                    return func(self, *args, **kwargs)
                else: 
                    raise error

        return wrapper

    @staticmethod
    def login(email, password):
        auth_response = requests.post(f'{AirZoneAPI.BASE_URL}/auth/login', json={
            "email": email,
            "password": password
        })
        auth_response.raise_for_status()
        auth_json = auth_response.json()
        update_settings({'token': auth_json['token'], 'refresh_token': auth_json['refreshToken']})

    def request_refresh_token(self):
        auth_response = requests.get(
            f'{self.BASE_URL}/auth/refreshToken/{self.refresh_token}')
        auth_response.raise_for_status()
        auth_json = auth_response.json()
        update_settings({'token': auth_json['token'], 'refresh_token': auth_json['refreshToken']})
        self.headers = {'Authorization': f'Bearer {auth_json["token"]}'}

    @retry_on_auth_error
    def get_installation_id(self):
        installations = requests.get(f'{self.BASE_URL}/installations',
                                     headers=self.headers)
        installations.raise_for_status()
        installations_json = installations.json()
        installation_id = installations_json['installations'][0][
            'installation_id']
        update_settings({'installation_id': installation_id})

        return installation_id

    @retry_on_auth_error
    def get_devices(self):
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
        update_settings({'devices': devices})

        return devices

    @retry_on_auth_error
    def get_device_status(self, device_id):
        status_response = requests.get(
            f'{self.BASE_URL}/devices/{device_id}/status',
            params={'installation_id': self.installation_id},
            headers=self.headers)
        status_response.raise_for_status()

        return status_response.json()

    @retry_on_auth_error
    def get_all_devices_status(self):
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {}
            for device_name, device_id in self.devices.items():
                    future = executor.submit(self.get_device_status, device_id)
                    futures[future] = device_name
            for future in as_completed(futures):
                device_name = futures[future]
                yield device_name, future.result()


