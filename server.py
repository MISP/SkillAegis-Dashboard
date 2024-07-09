#!/usr/bin/env python3

import collections
import functools
import json
import sys
import time
import zmq
import socketio
from aiohttp import web
import zmq.asyncio

import exercise as exercise_model
import notification as notification_model
import db
import config
from config import logger
import misp_api


ZMQ_MESSAGE_COUNT_LAST_TIMESPAN = 0
ZMQ_MESSAGE_COUNT = 0
ZMQ_LAST_TIME = None
USER_ACTIVITY = collections.defaultdict(int)


def debounce(debounce_seconds: int = 1):
    func_last_execution_time = {}
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            key = func.__name__
            if key not in func_last_execution_time:
                func_last_execution_time[key] = now
                return func(*args, **kwargs)
            elif now >= func_last_execution_time[key] + debounce_seconds:
                func_last_execution_time[key] = now
                return func(*args, **kwargs)
            else:
                return None
        return wrapper
    return decorator



# Initialize ZeroMQ context and subscriber socket
context = zmq.asyncio.Context()
zsocket = context.socket(zmq.SUB)
zmq_url = config.zmq_url
zsocket.connect(zmq_url)
zsocket.setsockopt_string(zmq.SUBSCRIBE, '')


# Initialize Socket.IO server
sio = socketio.AsyncServer(cors_allowed_origins='*', async_mode='aiohttp')
app = web.Application()
sio.attach(app)


async def index(request):
    with open('dist/index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')


@sio.event
async def connect(sid, environ):
    logger.debug("Client connected: %s", sid)

@sio.event
async def disconnect(sid):
    logger.debug("Client disconnected: %s", sid)

@sio.event
async def get_exercises(sid):
    return exercise_model.get_exercises()

@sio.event
async def get_selected_exercises(sid):
    return exercise_model.get_selected_exercises()

@sio.event
async def change_exercise_selection(sid, payload):
    return exercise_model.change_exercise_selection(payload['exercise_uuid'], payload['selected'])

@sio.event
async def get_progress(sid):
    return exercise_model.get_progress()

@sio.event
async def get_notifications(sid):
    return notification_model.get_notifications()

@sio.event
async def mark_task_completed(sid, payload):
    return exercise_model.mark_task_completed(int(payload['user_id']), payload['exercise_uuid'], payload['task_uuid'])

@sio.event
async def mark_task_incomplete(sid, payload):
    return exercise_model.mark_task_incomplete(int(payload['user_id']), payload['exercise_uuid'], payload['task_uuid'])

@sio.event
async def reset_all_exercise_progress(sid):
    return exercise_model.resetAllExerciseProgress()

@sio.event
async def reset_notifications(sid):
    return notification_model.reset_notifications()

@sio.event
async def get_diagnostic(sid):
    return await getDiagnostic()

@sio.event
async def get_users_activity(sid):
    return notification_model.get_users_activity()

@sio.event
async def toggle_verbose_mode(sid, payload):
    return notification_model.set_verbose_mode(payload['verbose'])

@sio.event
async def toggle_apiquery_mode(sid, payload):
    return notification_model.set_apiquery_mode(payload['apiquery'])

@sio.on('*')
async def any_event(event, sid, data={}):
    logger.info('>> Unhandled event %s', event)

async def handleMessage(topic, s, message):
    global ZMQ_MESSAGE_COUNT_LAST_TIMESPAN

    data = json.loads(message)

    if topic == 'misp_json_audit':
        user_id, email = notification_model.get_user_email_id_pair(data)
        if user_id is not None and user_id != 0 and '@' in email:
            if user_id not in db.USER_ID_TO_EMAIL_MAPPING:
                db.USER_ID_TO_EMAIL_MAPPING[user_id] = email
                await sio.emit('new_user', email)

        user_id, authkey = notification_model.get_user_authkey_id_pair(data)
        if user_id is not None and user_id != 0:
            if authkey not in db.USER_ID_TO_AUTHKEY_MAPPING:
                db.USER_ID_TO_AUTHKEY_MAPPING[user_id] = authkey
                return

        if notification_model.is_http_request(data):
            notification = notification_model.get_notification_message(data)
            if notification_model.is_accepted_notification(notification):
                notification_model.record_notification(notification)
                ZMQ_MESSAGE_COUNT_LAST_TIMESPAN += 1
                await sio.emit('notification', notification)
            if notification_model.is_accepted_user_activity(notification):
                user_id = notification_model.get_user_id(data)
                if user_id is not None:
                    USER_ACTIVITY[user_id] += 1

        user_id = notification_model.get_user_id(data)
        if user_id is not None:
            if exercise_model.is_accepted_query(data):
                context = get_context(topic, user_id, data)
                succeeded_once = await exercise_model.check_active_tasks(user_id, data, context)
                if succeeded_once:
                    await sendRefreshScore()


@debounce(debounce_seconds=1)
async def sendRefreshScore():
    await sio.emit('refresh_score')


def get_context(topic: str, user_id: int, data: dict) -> dict:
    context = {
        'zmq_topic': topic,
        'user_id': user_id,
        'user_email': db.USER_ID_TO_EMAIL_MAPPING.get(user_id, None),
        'user_authkey': db.USER_ID_TO_AUTHKEY_MAPPING.get(user_id, None),
    }
    if 'Log' in data:
        if 'request_is_rest' in data['Log']:
            context['request_is_rest'] = data['Log']['request_is_rest']
    elif 'authkey_id' in data:
        context['request_is_rest'] = True

    return context


async def getDiagnostic() -> dict:
    global ZMQ_MESSAGE_COUNT

    diagnostic = {}
    misp_version = await misp_api.getVersion()
    if misp_version is None:
        diagnostic['online'] = False
        return diagnostic
    diagnostic['version'] = misp_version
    misp_settings = await misp_api.getSettings()
    diagnostic['settings'] = misp_settings
    diagnostic['zmq_message_count'] = ZMQ_MESSAGE_COUNT
    return diagnostic


async def notification_history():
    global ZMQ_MESSAGE_COUNT_LAST_TIMESPAN
    while True:
        await sio.sleep(db.NOTIFICATION_HISTORY_FREQUENCY)
        notification_model.record_notification_history(ZMQ_MESSAGE_COUNT_LAST_TIMESPAN)
        ZMQ_MESSAGE_COUNT_LAST_TIMESPAN = 0
        payload = notification_model.get_notifications_history()
        await sio.emit('update_notification_history', payload)


async def record_users_activity():
    global USER_ACTIVITY

    while True:
        await sio.sleep(db.USER_ACTIVITY_FREQUENCY)
        for user_id, activity in USER_ACTIVITY.items():
            notification_model.record_user_activity(user_id, activity)
            USER_ACTIVITY[user_id] = 0
        payload = notification_model.get_users_activity()
        await sio.emit('update_users_activity', payload)


async def keepalive():
    global ZMQ_LAST_TIME
    while True:
        await sio.sleep(5)
        payload = {
            'zmq_last_time': ZMQ_LAST_TIME,
        }
        await sio.emit('keep_alive', payload)


async def backup_exercises_progress():
    while True:
        await sio.sleep(5)
        exercise_model.backup_exercises_progress()


# Function to forward zmq messages to Socket.IO
async def forward_zmq_to_socketio():
    global ZMQ_MESSAGE_COUNT, ZMQ_LAST_TIME

    while True:
        message = await zsocket.recv_string()
        topic, s, m = message.partition(" ")
        try:
            ZMQ_MESSAGE_COUNT += 1
            ZMQ_LAST_TIME = time.time()
            await handleMessage(topic, s, m)
        except Exception as e:
            print(e)
            logger.error('Error handling message %s', e)


async def init_app():
    sio.start_background_task(forward_zmq_to_socketio)
    sio.start_background_task(keepalive)
    sio.start_background_task(notification_history)
    sio.start_background_task(record_users_activity)
    sio.start_background_task(backup_exercises_progress)
    return app


app.router.add_static('/assets', 'dist/assets')
app.router.add_get('/', index)

if __name__ == "__main__":

    exercises_loaded = exercise_model.load_exercises()
    if not exercises_loaded:
        logger.critical('Could not load exercises')
        sys.exit(1)

    exercise_model.restore_exercices_progress()

    web.run_app(init_app(), host=config.server_host, port=config.server_port)
