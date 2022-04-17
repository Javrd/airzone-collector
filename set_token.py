#!/usr/bin/env python3
'''Get token and refresh token.
Use: ./set_token.py email password'''
import sys
from api import AirZoneAPI


if __name__ == '__main__':
  AirZoneAPI.login(sys.argv[1], sys.argv[2])
  
