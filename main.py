#!/usr/bin/env python3
import logging
from time import time

from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError

from api import AirZoneAPI
from models import DeviceStatus, InfluxAPI
from utils import send_to_discord

logger = logging.getLogger('airzone_collector')
logger.setLevel(logging.DEBUG)
logger.addFilter(send_to_discord)
client = InfluxDBClient(host='localhost', port=8086)

if __name__ == '__main__':
    try:
        airzone_client = AirZoneAPI()

        timestamp = round(time() * 1000)
        data = []
        for device_name, status_response in airzone_client.get_all_devices_status():
            device_status = DeviceStatus(status_response)
            data.extend(InfluxAPI.serialize(device_name, device_status, timestamp))
            for warning in device_status.warnings:
                logger.warning(warning.id)
            for error in device_status.errors:
                logger.error(error.id)

        client.write_points(data,
                            database='airzone',
                            time_precision='ms',
                            batch_size=10000,
                            protocol='json')
    except InfluxDBClientError as error:
        if error.code == 404:
            client.create_database('airzone')
        else:
            raise error
    except Exception as error:
        logger.exception('Unexpected error')
        raise error
