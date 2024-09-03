#!/usr/bin/env python3

import functools
import time
from backend.appConfig import logger


def debounce_check_active_tasks(debounce_seconds: int = 1):
    func_last_execution_time = {}
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            user_id = args[0]
            now = time.time()
            key = f"{user_id}_{func.__name__}"
            if key not in func_last_execution_time:
                func_last_execution_time[key] = now
                return func(*args, **kwargs)
            elif now >= func_last_execution_time[key] + debounce_seconds:
                func_last_execution_time[key] = now
                return func(*args, **kwargs)
            else:
                logger.debug(f">> Debounced for `{user_id}`")
                return None
        return wrapper
    return decorator
