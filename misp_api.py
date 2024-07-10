#!/usr/bin/env python3

import json
from datetime import timedelta
from typing import Union
from urllib.parse import urljoin
import asyncio
import requests # type: ignore
import requests.adapters # type: ignore
from requests_cache import CachedSession
from requests.packages.urllib3.exceptions import InsecureRequestWarning # type: ignore
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from config import misp_url, misp_apikey, misp_skipssl
from appConfig import logger, misp_settings

requestSession = CachedSession(cache_name='misp_cache', expire_after=timedelta(seconds=5))
adapterCache = requests.adapters.HTTPAdapter(pool_connections=50, pool_maxsize=50)
requestSession.mount('https://', adapterCache)
requestSession.mount('http://', adapterCache)


async def get(url, data={}, api_key=misp_apikey):
    headers = {
        'User-Agent': 'misp-exercise-dashboard',
        "Authorization": api_key,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    full_url = urljoin(misp_url, url)
    try:
        loop = asyncio.get_event_loop()
        job = lambda: requestSession.get(full_url, data=data, headers=headers, verify=not misp_skipssl)
        runningJob = loop.run_in_executor(None, job)
        response = await runningJob
    except requests.exceptions.ConnectionError as e:
        logger.info('Could not perform request on MISP. %s', e)
        return None
    except Exception as e:
        logger.warning('Could not perform request on MISP. %s', e)
    try:
        return response.json() if response.headers['content-type'].startswith('application/json') else response.text
    except requests.exceptions.JSONDecodeError:
        return response.text


async def post(url, data={}, api_key=misp_apikey):
    headers = {
        'User-Agent': 'misp-exercise-dashboard',
        "Authorization": api_key,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    full_url = urljoin(misp_url, url)
    try:
        loop = asyncio.get_event_loop()
        job = lambda: requestSession.post(full_url, data=json.dumps(data), headers=headers, verify=not misp_skipssl)
        runningJob = loop.run_in_executor(None, job)
        response = await runningJob
    except requests.exceptions.ConnectionError as e:
        logger.info('Could not perform request on MISP. %s', e)
        return None
    except Exception as e:
        logger.warning('Could not perform request on MISP. %s', e)
    try:
        return response.json() if response.headers['content-type'].startswith('application/json') else response.text
    except requests.exceptions.JSONDecodeError:
        return response.text


async def getEvent(event_id: int) -> Union[None, dict]:
    return await get(f'/events/view/{event_id}')


async def doRestQuery(authkey: str, request_method: str, url: str, payload: dict = {}) -> Union[None, dict]:
    if request_method == 'POST':
        return await post(url, payload, api_key=authkey)
    else:
        return await get(url, payload, api_key=authkey)


async def getVersion() -> Union[None, dict]:
    return await get(f'/servers/getVersion.json')


async def getSettings() -> Union[None, dict]:
    settings = await get(f'/servers/serverSettings.json')
    if not settings:
        return None
    data = {}
    for settingName, expectedSettingValue in misp_settings.items():
        data[settingName] = {
            'expected_value': expectedSettingValue,
            'value': None
        }
    for setting in settings.get('finalSettings', []):
        if setting['setting'] in misp_settings:
            data[setting['setting']]['value'] = setting['value']
    return data


async def remediateSetting(setting) ->dict:
    if setting in misp_settings:
        payload = {
            'value': misp_settings[setting],
        }
        return await post(f'/servers/serverSettingsEdit/{setting}', payload)