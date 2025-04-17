#!/usr/bin/env python3
from typing import Union
import jq

from backend.utils import eval_data_filtering
from backend.appConfig import logger
import backend.db as db


async def inject_checker_router(user_id: int, inject_evaluation: dict, data: dict, context: dict) -> bool:
    if inject_evaluation['evaluation_strategy'] == 'data_filtering':
        outcome = eval_data_filtering(inject_evaluation, data, context, False)
        return outcome
    return False
