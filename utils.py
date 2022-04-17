import logging
import os
import pathlib
import traceback

import requests
import yaml

cwd = pathlib.Path(__file__).parent.resolve()

def update_settings(new_settings: dict):
    with open(os.path.join(cwd, '.settings.yaml'), 'r') as f:
        settings = yaml.safe_load(f)
    if not settings:
        settings = {}
    settings.update(new_settings)

    with open(os.path.join(cwd, '.settings.yaml'), 'w') as f:
        yaml.dump(settings, f, default_flow_style=False, allow_unicode=True)

def ispar(number):
    return number % 2 == 0

def send_to_discord(record: logging.LogRecord):
    with open(os.path.join(cwd, '.settings.yaml'), 'r') as f:
        settings: dict = yaml.safe_load(f)
    url = settings.get('discord_webhook')
    if url:
        requests.post(url, json={'content': f'{record.getMessage()}\n{traceback.format_exc()}'})
    return True
