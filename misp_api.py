#!/usr/bin/env python3

import json
from datetime import timedelta
from typing import Union
from urllib.parse import urljoin
import requests # type: ignore
import requests.adapters # type: ignore
from requests_cache import CachedSession
from requests.packages.urllib3.exceptions import InsecureRequestWarning # type: ignore
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from config import misp_url, misp_apikey, misp_skipssl, logger

requestSession = CachedSession(cache_name='misp_cache', expire_after=timedelta(seconds=5))
adapterCache = requests.adapters.HTTPAdapter(pool_connections=50, pool_maxsize=50)
requestSession.mount('https://', adapterCache)
requestSession.mount('http://', adapterCache)


def get(url, data={}, api_key=misp_apikey):
    headers = {
        'User-Agent': 'misp-exercise-dashboard',
        "Authorization": api_key,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    full_url = urljoin(misp_url, url)
    try:
        response = requestSession.get(full_url, data=data, headers=headers, verify=not misp_skipssl)
    except requests.exceptions.ConnectionError as e:
        logger.info('Could not perform request on MISP.', e)
        return None
    return response.json() if response.headers['content-type'].startswith('application/json') else response.text


def post(url, data={}, api_key=misp_apikey):
    headers = {
        'User-Agent': 'misp-exercise-dashboard',
        "Authorization": api_key,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    full_url = urljoin(misp_url, url)
    try:
        response = requestSession.post(full_url, data=json.dumps(data), headers=headers, verify=not misp_skipssl)
    except requests.exceptions.ConnectionError as e:
        logger.info('Could not perform request on MISP.', e)
        return None
    return response.json() if response.headers['content-type'].startswith('application/json') else response.text


def getEvent(event_id: int) -> Union[None, dict]:
    return get(f'/events/view/{event_id}')


def doRestQuery(authkey: str, request_method: str, url: str, payload: dict = {}) -> Union[None, dict]:
    if request_method == 'POST':
        return post(url, payload, api_key=authkey)
    else:
        return get(url, payload, api_key=authkey)


def getVersion() -> Union[None, dict]:
    return get(f'/servers/getVersion.json')


def getSettings() -> Union[None, dict]:
    SETTING_TO_QUERY = [
        'Plugin.ZeroMQ_enable',
        'Plugin.ZeroMQ_audit_notifications_enable',
        'Plugin.ZeroMQ_event_notifications_enable',
        'Plugin.ZeroMQ_attribute_notifications_enable',
        'MISP.log_paranoid',
        'MISP.log_paranoid_skip_db',
        'MISP.log_paranoid_include_post_body',
        'MISP.log_auth',
        'Security.allow_unsafe_cleartext_apikey_logging',
    ]
    settings = get(f'/servers/serverSettings.json')
    if not settings:
        return None
    return {
        setting['setting']: setting['value'] for setting in settings.get('finalSettings', []) if setting['setting'] in SETTING_TO_QUERY
    }