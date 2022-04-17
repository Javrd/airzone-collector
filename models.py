import json
from typing import List
from influxdb import InfluxDBClient


class Error:
    id: str

    def __init__(self, json) -> None:
        self.id = json.get('id')


class Temp:
    fah: float
    celsius: float

    def __init__(self, json) -> None:
        self.fah = json.get('fah') if 'fah' in json else None
        self.celsius = json.get('celsius') if 'celsius' in json else None


class Manufacturer:
    id: int
    text: str

    def __init__(self, json) -> None:
        self.id = json.get('id')
        self.text = json.get('text')


class DeviceStatus:
    MODES = {
        None: "",
        0: "Stop",
        1: "Auto",
        2: "Cooling",
        3: "Heating",
        4: "Ventilation",
        5: "Dehumidifier/Dry",
        6: "Emergency Heat",
        7: "Heat air",
        8: "Heat radiant",
        9: "Heat combined",
        10: "Cooling air",
        11: "Cooling radiant",
        12: "Cooling combined"
    }
    humidity: int
    block_mode: bool
    block_off: bool
    block_on: bool
    block_autospeed: bool
    block_autotemp: bool
    block_dryspeed: bool
    block_drytemp: bool
    block_fantemp: bool
    block_setpoint: bool
    manufacturer: Manufacturer
    aidooit: bool
    machineready: bool
    is_connected: bool
    power: bool
    mode: str
    mode_available: List[str]
    auto_mode: str
    speed_values: List[int]
    speed_type: int
    step: Temp
    range_sp_cool_air_min: Temp
    range_sp_cool_air_max: Temp
    range_sp_hot_air_max: Temp
    range_sp_hot_air_min: Temp
    range_sp_dry_air_max: Temp
    range_sp_dry_air_min: Temp
    range_sp_vent_air_max: Temp
    range_sp_vent_air_min: Temp
    range_sp_emerheat_air_min: Temp
    range_sp_emerheat_air_max: Temp
    range_sp_auto_air_min: Temp
    range_sp_auto_air_max: Temp
    range_sp_stop_air_min: Temp
    range_sp_stop_air_max: Temp
    setpoint_air_heat: Temp
    setpoint_air_emerheat: Temp
    setpoint_air_cool: Temp
    setpoint_air_vent: Temp
    setpoint_air_dry: Temp
    setpoint_air_auto: Temp
    setpoint_air_stop: Temp
    double_sp: bool
    local_temp: Temp
    speed_conf: int
    eco_conf: str
    eco_values: List[str]
    usermode_conf: str
    usermode_values: List[str]
    aq_mode_conf: str
    aq_mode_values: List[str]
    warnings: List[Error]
    errors: List[Error]
    aqpm1_0: int
    aqpm2_0: int
    aqpm10: int
    aq_quality: str

    def __init__(self, json_response) -> None:
        self.humidity = json_response.get('humidity')
        self.block_mode = json_response.get('block_mode')
        self.block_off = json_response.get('block_off')
        self.block_on = json_response.get('block_on')
        self.block_autospeed = json_response.get('block_autospeed')
        self.block_autotemp = json_response.get('block_autotemp')
        self.block_dryspeed = json_response.get('block_dryspeed')
        self.block_drytemp = json_response.get('block_drytemp')
        self.block_fantemp = json_response.get('block_fantemp')
        self.block_setpoint = json_response.get('block_setpoint')
        self.manufacturer = Manufacturer(json_response.get('manufacturer', {}))
        self.aidooit = json_response.get('aidooit')
        self.machineready = json_response.get('machineready')
        self.is_connected = json_response.get('is_connected')
        self.power = json_response.get('power')
        self.mode = DeviceStatus.MODES[json_response.get('mode')]
        self.mode_available = [DeviceStatus.MODES[mode] for mode in json_response.get('mode_available')]
        self.auto_mode = DeviceStatus.MODES[json_response.get('auto_mode')]
        self.speed_values = json_response.get('speed_values')
        self.speed_type = json_response.get('speed_type')
        self.step = Temp(json_response.get('step', {}))
        self.range_sp_cool_air_min = Temp(json_response.get('range_sp_cool_air_min', {}))
        self.range_sp_cool_air_max = Temp(json_response.get('range_sp_cool_air_max', {}))
        self.range_sp_hot_air_max = Temp(json_response.get('range_sp_hot_air_max', {}))
        self.range_sp_hot_air_min = Temp(json_response.get('range_sp_hot_air_min', {}))
        self.range_sp_dry_air_max = Temp(json_response.get('range_sp_dry_air_max', {}))
        self.range_sp_dry_air_min = Temp(json_response.get('range_sp_dry_air_min', {}))
        self.range_sp_vent_air_max = Temp(json_response.get('range_sp_vent_air_max', {}))
        self.range_sp_vent_air_min = Temp(json_response.get('range_sp_vent_air_min', {}))
        self.range_sp_emerheat_air_min = Temp(json_response.get('range_sp_emerheat_air_min', {}))
        self.range_sp_emerheat_air_max = Temp(json_response.get('range_sp_emerheat_air_max', {}))
        self.range_sp_auto_air_min = Temp(json_response.get('range_sp_auto_air_min', {}))
        self.range_sp_auto_air_max = Temp(json_response.get('range_sp_auto_air_max', {}))
        self.range_sp_stop_air_min = Temp(json_response.get('range_sp_stop_air_min', {}))
        self.range_sp_stop_air_max = Temp(json_response.get('range_sp_stop_air_max', {}))
        self.setpoint_air_heat = Temp(json_response.get('setpoint_air_heat', {}))
        self.setpoint_air_emerheat = Temp(json_response.get('setpoint_air_emerheat', {}))
        self.setpoint_air_cool = Temp(json_response.get('setpoint_air_cool', {}))
        self.setpoint_air_vent = Temp(json_response.get('setpoint_air_vent', {}))
        self.setpoint_air_dry = Temp(json_response.get('setpoint_air_dry', {}))
        self.setpoint_air_auto = Temp(json_response.get('setpoint_air_auto', {}))
        self.setpoint_air_stop = Temp(json_response.get('setpoint_air_stop', {}))
        self.double_sp = json_response.get('double_sp')
        self.local_temp = Temp(json_response.get('local_temp', {}))
        self.speed_conf = json_response.get('speed_conf')
        self.eco_conf = json_response.get('eco_conf')
        self.eco_values = json_response.get('eco_values')
        self.usermode_conf = json_response.get('usermode_conf')
        self.usermode_values = json_response.get('usermode_values')
        self.aq_mode_conf = json_response.get('aq_mode_conf')
        self.aq_mode_values = json_response.get('aq_mode_values')
        self.warnings = [Error(warning) for warning in json_response.get('warnings')] if 'warnings' in json_response else []
        self.errors = [Error(error) for error in json_response.get('errors')] if 'errors' in json_response else []
        self.aqpm1_0 = json_response.get('aqpm1_0')
        self.aqpm2_0 = json_response.get('aqpm2_0')
        self.aqpm10 = json_response.get('aqpm10')
        self.aq_quality = json_response.get('aq_quality')


class InfluxAPI(InfluxDBClient):
    @classmethod
    def serialize(cls, device_name: str, device_status: DeviceStatus, timestamp: int):        
        data = []
        tags = {
                "location": device_name,
                "mode": device_status.mode,
                "power": device_status.power
        }
        temp = device_status.local_temp.celsius
        data.append(cls.__set_point("temperature", tags, temp, timestamp))
        data.append(cls.__set_point("humidity", tags, device_status.humidity, timestamp))
        return data
    
    @staticmethod
    def __set_point(mesurement, tags, value, timestamp):
        return {
            "measurement": mesurement,
            "tags": tags,
            "fields": {
                "value": value
            },
            "time": timestamp
        }