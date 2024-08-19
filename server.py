#!/usr/bin/env python3

import collections
import functools
import json
import argparse
import os
from pathlib import Path
import sys
import time
import traceback
import zmq
import socketio
from aiohttp import web
import zmq.asyncio

import exercise as exercise_model
import notification as notification_model
import db
import config
from appConfig import logger
import misp_api


ZMQ_LOG_FILE = None
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


def timer():
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            t1 = time.time()
            res = func(*args, **kwargs)
            elapsed = time.time() - t1
            if elapsed > 0.1:
                print(elapsed)
            return res
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

async def favicon(request):
    with open('dist/favicon.ico', 'rb') as f:
        return web.Response(body=f.read(), content_type='image/x-icon')


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
async def reset_all(sid):
    return exercise_model.resetAllCommand()

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

@sio.event
async def remediate_setting(sid, payload):
    return await doSettingRemediation(payload['name'])

@sio.event
async def reload_from_disk(sid):
    return exercise_model.reloadFromDisk()

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
                checking_task = exercise_model.check_active_tasks(user_id, data, context)
                if checking_task is not None:  # Make sure check_active_tasks was not debounced
                    succeeded_once = await checking_task
                    if succeeded_once:
                        sendRefreshScoreTask = sendRefreshScore()
                        await sendRefreshScoreTask if sendRefreshScoreTask is not None else None  # Make sure check_active_tasks was not debounced


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


async def doSettingRemediation(setting) -> dict:
    result = await misp_api.remediateSetting(setting)
    return result


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


# Function to forward zmq messages to Socket.IO
async def forward_fake_zmq_to_socketio():
    global ZMQ_MESSAGE_COUNT, ZMQ_LAST_TIME, ZMQ_LOG_FILE
    filename = ZMQ_LOG_FILE
    line_number = sum(1 for _ in open(filename))
    print(f'Preparing to feed {line_number} lines..')
    await sio.sleep(2)

    print('Feeding started')
    line_count = 0
    last_print = time.time()
    with open(filename) as f:
        for line in f:
            line_count += 1
            now = time.time()
            if line_count % (int(line_number/100)) == 0 or (now - last_print >= 5):
                last_print = now
                print(f'Feeding {line_count} / {line_number} - ({100* line_count / line_number:.1f}%)')
            split = line.split(' ', 1)
            topic = split[0]
            s = ''
            m = split[1]
            if topic != 'misp_json_self':
                await sio.sleep(0.01)
            try:
                ZMQ_MESSAGE_COUNT += 1
                ZMQ_LAST_TIME = time.time()
                await handleMessage(topic, s, m)
            except Exception as e:
                print(e)
                print(line)
                print(traceback.format_exc())
                logger.error('Error handling message: %s', e)
                await sio.sleep(5)
    print('Feeding done.')


async def init_app(zmq_log_file=None):
    global ZMQ_LOG_FILE

    if zmq_log_file is not None:
        ZMQ_LOG_FILE = zmq_log_file
        sio.start_background_task(forward_fake_zmq_to_socketio)
    else:
        exercise_model.restore_exercices_progress()
        sio.start_background_task(forward_zmq_to_socketio)
    sio.start_background_task(keepalive)
    sio.start_background_task(notification_history)
    sio.start_background_task(record_users_activity)
    sio.start_background_task(backup_exercises_progress)
    return app


app.router.add_static('/assets', 'dist/assets')
app.router.add_get('/', index)
app.router.add_get('/favicon.ico', favicon)

def main():
    parser = argparse.ArgumentParser(description='Parse command-line arguments for SkillAegis Dashboard.')

    parser.add_argument('--host', type=str, required=False, default=config.server_host, help='The host to listen to')
    parser.add_argument('--port', type=int, required=False, default=config.server_port, help='The port to listen to')
    parser.add_argument('--exercise_folder', type=str, required=False, default=config.exercise_directory, help='The folder containing all exercises')
    parser.add_argument('--zmq_log_file', type=str, required=False, default=None, help='A ZMQ log file to replay. Will disable the ZMQ subscription defined in the settings.')

    args = parser.parse_args()

    # Validate exercise_folder
    if not os.path.isdir(args.exercise_folder):
        parser.error(f"The specified exercise_folder does not exist or is not a directory: {args.exercise_folder}")
    else:
        exercise_model.ACTIVE_EXERCISES_DIR = Path(args.exercise_folder)

    if args.zmq_log_file and not os.path.isfile(args.zmq_log_file):
        parser.error(f"The specified zmq_log_file does not exist or is not a file: {args.zmq_log_file}")

    exercises_loaded = exercise_model.load_exercises()
    if not exercises_loaded:
        logger.critical('Could not load exercises')
        sys.exit(1)

    web.run_app(init_app(args.zmq_log_file), host=args.host, port=args.port)

if __name__ == "__main__":
    main()
