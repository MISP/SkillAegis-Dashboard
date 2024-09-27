
import sys

live_logs_accepted_scope = {
    'events': ['add', 'edit', 'delete', 'restSearch',],
    'attributes': ['add', 'add_attachment', 'edit', 'revise_object', 'delete', 'restSearch',],
    'eventReports': ['add', 'edit', 'delete',],
    'tags': '*',
}

user_activity_accepted_scope = {
    'events': ['view', 'add', 'edit', 'delete', 'restSearch',],
    'attributes': ['add', 'add_attachment', 'edit', 'delete', 'restSearch',],
    'objects': ['add', 'edit', 'revise_object', 'delete',],
    'eventReports': ['view', 'add', 'edit', 'delete',],
    'tags': '*',
}

misp_settings = {
    'Plugin.ZeroMQ_enable': True,
    'Plugin.ZeroMQ_audit_notifications_enable': True,
    'Plugin.ZeroMQ_event_notifications_enable': True,
    'Plugin.ZeroMQ_attribute_notifications_enable': True,
    'MISP.log_paranoid': True,
    'MISP.log_paranoid_skip_db': True,
    'MISP.log_paranoid_include_post_body': True,
    'MISP.log_auth': True,
    'Security.allow_unsafe_cleartext_apikey_logging': True,
}

import logging
logger = logging.getLogger('SkillAegis')
format = '[%(levelname)s] %(asctime)s - %(message)s'
formatter = logging.Formatter(format)

fh = logging.FileHandler(filename='SkillAegis.log', encoding='utf-8')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

# logging.basicConfig(filename='SkillAegis.log', encoding='utf-8', level=logging.DEBUG, format=format)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
logger.addHandler(ch)
