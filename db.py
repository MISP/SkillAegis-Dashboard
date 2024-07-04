#!/usr/bin/env python3

import collections


USER_ID_TO_EMAIL_MAPPING = {}
USER_ID_TO_AUTHKEY_MAPPING = {}
ALL_EXERCISES = []
SELECTED_EXERCISES = []
INJECT_BY_UUID = {}
INJECT_SEQUENCE_BY_INJECT_UUID = {}
INJECT_REQUIREMENTS_BY_INJECT_UUID = {}
EXERCISES_STATUS = {}
PROGRESS = {
}
NOTIFICATION_BUFFER_SIZE = 30
NOTIFICATION_MESSAGES = collections.deque([], NOTIFICATION_BUFFER_SIZE)

NOTIFICATION_HISTORY_BUFFER_RESOLUTION_PER_MIN = 3
NOTIFICATION_HISTORY_BUFFER_TIMESPAN_MIN = 60
NOTIFICATION_HISTORY_FREQUENCY = NOTIFICATION_HISTORY_BUFFER_TIMESPAN_MIN / NOTIFICATION_HISTORY_BUFFER_RESOLUTION_PER_MIN
notification_history_size = NOTIFICATION_HISTORY_BUFFER_RESOLUTION_PER_MIN * NOTIFICATION_HISTORY_BUFFER_TIMESPAN_MIN
NOTIFICATION_HISTORY = collections.deque([], notification_history_size)
NOTIFICATION_HISTORY.extend([0] * notification_history_size)

def resetNotificationMessage():
   global NOTIFICATION_MESSAGES
   NOTIFICATION_MESSAGES = collections.deque([], NOTIFICATION_BUFFER_SIZE)

def resetNotificationHistory():
   global NOTIFICATION_HISTORY
   NOTIFICATION_HISTORY = collections.deque([], notification_history_size)
   NOTIFICATION_HISTORY.extend([0] * notification_history_size)