import sys
import os
import requests
from get_data import AirZoneAPI


if __name__ == '__main__':
  auth_response = requests.post(f'{AirZoneAPI.BASE_URL}/auth/login', json={
    "email": sys.argv[1],
    "password": sys.argv[2]
  })
  auth_response.raise_for_status()
  auth_json = auth_response.json()
  AirZoneAPI.update_settings('token', auth_json['token'])
  AirZoneAPI.update_settings('refresh_token', auth_json['refreshToken'])
  
