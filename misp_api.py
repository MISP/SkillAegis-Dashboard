#!/usr/bin/env python3

import json
from typing import Union
from urllib.parse import urljoin
import requests # type: ignore
import requests.adapters # type: ignore
from requests.packages.urllib3.exceptions import InsecureRequestWarning # type: ignore
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from config import misp_url, misp_apikey, misp_skipssl


def get(url, data={}, api_key=misp_apikey):
    headers = {
        'User-Agent': 'misp-exercise-dashboard',
        "Authorization": api_key,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    full_url = urljoin(misp_url, url)
    response = requests.get(full_url, data=data, headers=headers, verify=not misp_skipssl)
    return response.json() if response.headers['content-type'] == 'application/json' else response.text


def post(url, data={}, api_key=misp_apikey):
    headers = {
        'User-Agent': 'misp-exercise-dashboard',
        "Authorization": api_key,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    full_url = urljoin(misp_url, url)
    response = requests.post(full_url, data=json.dumps(data), headers=headers, verify=not misp_skipssl)
    return response.json() if response.headers['content-type'] == 'application/json' else response.text


def getEvent(event_id: int) -> Union[None, dict]:
    return get(f'/events/view/{event_id}')


def doRestQuery(authkey: str, request_method: str, url: str, payload: dict = {}) -> Union[None, dict]:
    if request_method == 'POST':
        return post(url, payload, api_key=authkey)
    else:
        return get(url, payload, api_key=authkey)
