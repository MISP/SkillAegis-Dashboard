#!/usr/bin/env python3

import collections
from typing import Union

USER_ID_TO_EMAIL_MAPPING = {}
USER_ID_TO_AUTHKEY_MAPPING = {}

ALL_EXERCISES = []
SELECTED_EXERCISES = []
INJECT_BY_UUID = {}
INJECT_SEQUENCE_BY_INJECT_UUID = {}
INJECT_REQUIREMENTS_BY_INJECT_UUID = {}
EXERCISES_STATUS = {}

NOTIFICATION_BUFFER_SIZE = 30
NOTIFICATION_MESSAGES = collections.deque([], NOTIFICATION_BUFFER_SIZE)

NOTIFICATION_HISTORY_BUFFER_RESOLUTION_PER_MIN = 12
NOTIFICATION_HISTORY_BUFFER_TIMESPAN_MIN = 20
NOTIFICATION_HISTORY_FREQUENCY = 60 / NOTIFICATION_HISTORY_BUFFER_RESOLUTION_PER_MIN
notification_history_buffer_size = NOTIFICATION_HISTORY_BUFFER_RESOLUTION_PER_MIN * NOTIFICATION_HISTORY_BUFFER_TIMESPAN_MIN
NOTIFICATION_HISTORY = collections.deque([], notification_history_buffer_size)
NOTIFICATION_HISTORY.extend([0] * notification_history_buffer_size)

USER_ACTIVITY_BUFFER_RESOLUTION_PER_MIN = 2
USER_ACTIVITY_TIMESPAN_MIN = 20
USER_ACTIVITY_FREQUENCY = 60 / USER_ACTIVITY_BUFFER_RESOLUTION_PER_MIN
USER_ACTIVITY = {}
user_activity_buffer_size = USER_ACTIVITY_BUFFER_RESOLUTION_PER_MIN * USER_ACTIVITY_TIMESPAN_MIN


def resetNotificationMessage():
   global NOTIFICATION_MESSAGES
   NOTIFICATION_MESSAGES = collections.deque([], NOTIFICATION_BUFFER_SIZE)

def resetNotificationHistory():
   global NOTIFICATION_HISTORY
   NOTIFICATION_HISTORY = collections.deque([], notification_history_buffer_size)
   NOTIFICATION_HISTORY.extend([0] * notification_history_buffer_size)

def addUserActivity(user_id: int, count: int):
   global USER_ACTIVITY, USER_ACTIVITY_TIMESPAN_MIN

   if user_id not in USER_ACTIVITY:
      USER_ACTIVITY[user_id] = collections.deque([], user_activity_buffer_size)
      USER_ACTIVITY[user_id].extend([0] * user_activity_buffer_size)
   USER_ACTIVITY[user_id].append(count)

def resetUserActivity():
   for user_id in USER_ACTIVITY.keys():
      USER_ACTIVITY[user_id] = collections.deque([], user_activity_buffer_size)
      USER_ACTIVITY[user_id].extend([0] * user_activity_buffer_size)