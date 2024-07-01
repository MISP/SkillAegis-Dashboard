#!/usr/bin/env python3

import json
import sys
import zmq
import socketio
import eventlet
from pprint import pprint
from eventlet.green import zmq as gzmq

import exercise as exercise_model
import notification as notification_model
import db
import misp_api


# Initialize ZeroMQ context and subscriber socket
context = gzmq.Context()
zsocket = context.socket(gzmq.SUB)
zmq_url = "tcp://localhost:50000"  # Update this with your zmq publisher address
zsocket.connect(zmq_url)
zsocket.setsockopt_string(gzmq.SUBSCRIBE, '')


# Initialize Socket.IO server
sio = socketio.Server(cors_allowed_origins='*', async_mode='eventlet')
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'dist/index.html'},
    '/assets': './dist/assets',
})

@sio.event
def connect(sid, environ):
    print("Client connected: ", sid)

@sio.event
def disconnect(sid):
    print("Client disconnected: ", sid)

@sio.event
def get_exercises(sid):
    return exercise_model.get_exercises()

@sio.event
def get_selected_exercises(sid):
    return exercise_model.get_selected_exercises()

@sio.event
def change_exercise_selection(sid, payload):
    return exercise_model.change_exercise_selection(payload['exercise_uuid'], payload['selected'])

@sio.event
def get_progress(sid):
    return exercise_model.get_progress()

@sio.event
def get_notifications(sid):
    return notification_model.get_notifications()

@sio.event
def mark_task_completed(sid, payload):
    return exercise_model.mark_task_completed(int(payload['user_id']), payload['exercise_uuid'], payload['task_uuid'])

@sio.event
def mark_task_incomplete(sid, payload):
    return exercise_model.mark_task_incomplete(int(payload['user_id']), payload['exercise_uuid'], payload['task_uuid'])

@sio.event
def reset_all_exercise_progress(sid):
    return exercise_model.resetAllExerciseProgress()

@sio.event
def get_diagnostic(sid):
    return getDiagnostic()

@sio.event
def toggle_verbose_mode(sid, payload):
    return notification_model.set_verbose_mode(payload['verbose'])

@sio.on('*')
def any_event(event, sid, data={}):
    print('>> Unhandled event', event)

def handleMessage(topic, s, message):
    data = json.loads(message)

    if topic == 'misp_json_audit':
        user_id, email = notification_model.get_user_email_id_pair(data)
        if user_id is not None and '@' in email:
            if user_id not in db.USER_ID_TO_EMAIL_MAPPING:
                db.USER_ID_TO_EMAIL_MAPPING[user_id] = email
                sio.emit('new_user', email)

        user_id, authkey = notification_model.get_user_authkey_id_pair(data)
        if user_id is not None:
            if authkey not in db.USER_ID_TO_AUTHKEY_MAPPING:
                db.USER_ID_TO_AUTHKEY_MAPPING[user_id] = authkey
                return

        if notification_model.is_http_request(data):
            notification = notification_model.get_notification_message(data)
            if notification_model.is_accepted_notification(notification):
                notification_model.record_notification(notification)
                sio.emit('notification', notification)

        user_id = notification_model.get_user_id(data)
        if user_id is not None:
            if exercise_model.is_accepted_query(data):
                context = get_context(data)
                succeeded_once = exercise_model.check_active_tasks(user_id, data, context)
                if succeeded_once:
                    sio.emit('refresh_score')


def get_context(data: dict) -> dict:
    context = {}
    if 'Log' in data:
        if 'request_is_rest' in data['Log']:
            context['request_is_rest'] = data['Log']['request_is_rest']
    elif 'authkey_id' in data:
        context['request_is_rest'] = True

    return context


def getDiagnostic() -> dict:
    diagnostic = {}
    misp_version = misp_api.getVersion()
    if misp_version is None:
        diagnostic['online'] = False
        return diagnostic
    diagnostic['version'] = misp_version
    misp_settings = misp_api.getSettings()
    diagnostic['settings'] = misp_settings
    return diagnostic


# Function to forward zmq messages to Socket.IO
def forward_zmq_to_socketio():
    while True:
        message = zsocket.recv_string()
        topic, s, m = message.partition(" ")
        try:
            handleMessage(topic, s, m)
        except Exception as e:
            print(e)


if __name__ == "__main__":

    exercises_loaded = exercise_model.load_exercises()
    if not exercises_loaded:
        print('Could not load exercises')
        sys.exit(1)

    # Start the forwarding in a separate thread
    eventlet.spawn_n(forward_zmq_to_socketio)

    # Run the Socket.IO server
    eventlet.wsgi.server(eventlet.listen(('127.0.0.1', 4000)), app)
