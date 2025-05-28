#!/usr/bin/env python3

import functools
import time
from pathlib import Path
import json
import re
from typing import Union
import jq

from backend.utils import debounce_check_active_tasks
import backend.misp_api as misp_api
from backend.appConfig import logger
import backend.config as config
import backend.db as db
import backend.leaderboard as leadboard

from backend.target_tools.misp.exercise import inject_checker_router as inject_checker_router_misp
from backend.target_tools.suricata.exercise import inject_checker_router as inject_checker_router_suricata
from backend.target_tools.webhook.exercise import inject_checker_router as inject_checker_router_webhook


ACTIVE_EXERCISES_DIR = Path(config.exercise_directory)
LAST_BACKUP = {}


def load_exercises() -> bool:
    db.ALL_EXERCISES = read_exercise_dir()
    if not is_validate_exercises(db.ALL_EXERCISES):
        logger.error('Issue while validating exercises')
        return False
    init_inject_flow()
    init_exercises_tasks()
    return True


def read_exercise_dir():
    target_dir = ACTIVE_EXERCISES_DIR
    json_files = target_dir.glob("*.json")
    exercises = []
    for json_file in json_files:
        with open(json_file) as f:
            try:
                parsed_exercise = json.load(f)
                exercises.append(parsed_exercise)
            except json.JSONDecodeError as e:
                print(f'Could not parse {json_file}', str(e))
            except Exception as e:
                print(f'Error while reading {json_file}', str(e))
    return exercises


def backup_exercises_progress():
    global LAST_BACKUP
    toBackup = {
        "EXERCISES_STATUS": db.EXERCISES_STATUS,
        "SELECTED_EXERCISES": db.SELECTED_EXERCISES,
        "USER_ID_TO_EMAIL_MAPPING": db.USER_ID_TO_EMAIL_MAPPING,
        "EMAIL_TO_USER_ID_MAPPING": db.EMAIL_TO_USER_ID_MAPPING,
        "USER_ID_TO_AUTHKEY_MAPPING": db.USER_ID_TO_AUTHKEY_MAPPING,
    }
    toBackup = json.dumps(toBackup, sort_keys=True)
    if toBackup != LAST_BACKUP: # Easy way to compared these 2 nested dict
        with open('backup.json', 'w') as f:
            f.write(toBackup)
            LAST_BACKUP = toBackup


def restore_exercices_progress():
    try:

        with open('backup.json', 'r') as f:
            data = json.load(f)
            db.EXERCISES_STATUS = data['EXERCISES_STATUS']
            db.SELECTED_EXERCISES = data['SELECTED_EXERCISES']
            db.USER_ID_TO_EMAIL_MAPPING = {}
            for user_id_str, email in data['USER_ID_TO_EMAIL_MAPPING'].items():
                db.USER_ID_TO_EMAIL_MAPPING[int(user_id_str)] = email
            db.EMAIL_TO_USER_ID_MAPPING = {}
            for email, user_id_str in data["EMAIL_TO_USER_ID_MAPPING"].items():
                db.EMAIL_TO_USER_ID_MAPPING[email] = int(user_id_str)
            db.USER_ID_TO_AUTHKEY_MAPPING = {}
            for user_id_str, authkey in data['USER_ID_TO_AUTHKEY_MAPPING'].items():
                db.USER_ID_TO_AUTHKEY_MAPPING[int(user_id_str)] = authkey
    except Exception as e:
        logger.info(f"Could not restore exercise progress: {str(e)}")
        resetAll()

    if len(db.EXERCISES_STATUS) == 0:
        init_exercises_tasks()


def resetAll():
    db.EXERCISES_STATUS = {}
    db.SELECTED_EXERCISES = []
    db.USER_ID_TO_EMAIL_MAPPING = {}
    db.EMAIL_TO_USER_ID_MAPPING = {}
    db.USER_ID_TO_AUTHKEY_MAPPING = {}
    init_exercises_tasks()

def reloadFromDisk():
    resetAll()
    load_exercises()


def is_validate_exercises(exercises: list) -> bool:
    exercises_uuid = set()
    tasks_uuid = set()
    exercise_by_uuid = {}
    task_by_uuid = {}
    for exercise in exercises:
        e_uuid = exercise['exercise']['uuid']
        if e_uuid in exercises_uuid:
            logger.error(f"Duplicated UUID {e_uuid}. ({exercise['exercise']['name']}, {exercise_by_uuid[e_uuid]['exercise']['name']})")
            return False
        exercises_uuid.add(e_uuid)
        exercise_by_uuid[e_uuid] = exercise
        for inject in exercise['injects']:
            t_uuid = inject['uuid']
            if t_uuid in tasks_uuid:
                logger.error(f"Duplicated UUID {t_uuid}. ({inject['name']}, {task_by_uuid[t_uuid]['name']})")
                return False
            tasks_uuid.add(t_uuid)
            task_by_uuid[t_uuid] = inject

            for inject_evaluation in inject.get('inject_evaluation', []):
                if inject_evaluation.get('evaluation_strategy', None) == 'data_filtering':
                    for evaluation in inject_evaluation.get('parameters', []):
                        jq_path = list(evaluation.keys())[0]
                        try:
                            jq.compile(jq_path)
                        except ValueError as e:
                            logger.error(f"[{t_uuid} :: {inject['name']}] Could not compile jq path `{jq_path}`\n", e)
                            return False

    return True


def init_inject_flow():
    for exercise in db.ALL_EXERCISES:
        for inject in exercise['injects']:
            inject['exercise_uuid'] = exercise['exercise']['uuid']
            db.INJECT_BY_UUID[inject['uuid']] = inject

    for exercise in db.ALL_EXERCISES:
        for inject_flow in exercise['inject_flow']:
            db.INJECT_REQUIREMENTS_BY_INJECT_UUID[inject_flow['inject_uuid']] = inject_flow['requirements']
            db.INJECT_SEQUENCE_BY_INJECT_UUID[inject_flow['inject_uuid']] = []
            for sequence in inject_flow['sequence'].get('followed_by', []):
                db.INJECT_SEQUENCE_BY_INJECT_UUID[inject_flow['inject_uuid']].append(sequence)


def init_exercises_tasks():
    for exercise in db.ALL_EXERCISES:
        max_score = 0
        tasks = {}
        for inject in exercise['injects']:
            score = 0
            try:
                for inject_eval in inject['inject_evaluation']:
                    score += inject_eval['score_range'][1]
            except KeyError:
                pass
            max_score += score
            tasks[inject['uuid']] = {
                "name": inject['name'],
                "uuid": inject['uuid'],
                "completed_by_user": [],
                "score": score,
            }
        db.EXERCISES_STATUS[exercise['exercise']['uuid']] = {
            'uuid': exercise['exercise']['uuid'],
            'name': exercise['exercise']['name'],
            'tasks': tasks,
            'max_score': max_score,
        }


def get_exercises():
    exercises = []
    for exercise in db.ALL_EXERCISES:
        tasks = []
        for inject in exercise['injects']:
            score = db.EXERCISES_STATUS[exercise['exercise']['uuid']]['tasks'][inject['uuid']]['score']
            requirements = db.INJECT_REQUIREMENTS_BY_INJECT_UUID[inject['uuid']]
            tasks.append(
                {
                    "name": inject['name'],
                    "uuid": inject['uuid'],
                    "description": inject.get('description', ''),
                    "score": score,
                    "requirements": requirements,
                }
            )
        exercises.append(
            {
                "name": exercise['exercise']['name'],
                "uuid": exercise['exercise']['uuid'],
                "description": exercise['exercise']['description'],
                "level": exercise['exercise']['meta'].get('level', 'beginner'),
                "priority": exercise['exercise']['meta'].get('priority', 50),
                "tasks": tasks,
            }
        )
    exercises = sorted(exercises, key=lambda d: d['priority'])
    return exercises


def get_selected_exercises() -> list:
    return db.SELECTED_EXERCISES


def get_all_exercises() -> list:
    return db.ALL_EXERCISES


def change_exercise_selection(exercise_uuid: str, selected: bool):
    if selected:
        if exercise_uuid not in db.SELECTED_EXERCISES:
            db.SELECTED_EXERCISES.append(exercise_uuid)
    else:
        if exercise_uuid in db.SELECTED_EXERCISES:
            db.SELECTED_EXERCISES.remove(exercise_uuid)

    from backend.server import start_timed_injects
    start_timed_injects()


def resetAllExerciseProgress():
    for user_id in db.USER_ID_TO_EMAIL_MAPPING.keys():
        for exercise_status in db.EXERCISES_STATUS.values():
            for task in exercise_status['tasks'].values():
                mark_task_incomplete(user_id, exercise_status['uuid'], task['uuid'])
    backup_exercises_progress()


def resetAllCommand():
    resetAll()
    backup_exercises_progress()


def is_user_email_known(user_id: int):
    return db.USER_ID_TO_EMAIL_MAPPING.get(user_id, None) is not None

def is_user_authkey_known(user_id: int):
    return db.USER_ID_TO_AUTHKEY_MAPPING.get(user_id, None) is not None

def is_user_fully_known(user_id: int):
    return is_user_email_known(user_id) and is_user_authkey_known(user_id)


def get_completed_tasks_for_user(user_id: int):
    completion = get_completion_for_users().get(user_id, {})
    completed_tasks = {}
    for exec_uuid, tasks in completion.items():
        completed_tasks[exec_uuid] = [task_uuid for task_uuid, completed in tasks.items() if completed]
    return completed_tasks

def get_incomplete_tasks_for_user(user_id: int):
    completion = get_completion_for_users().get(user_id, {})
    incomplete_tasks = {}
    for exec_uuid, tasks in completion.items():
        incomplete_tasks[exec_uuid] = [task_uuid for task_uuid, completed in tasks.items() if not completed]
    return incomplete_tasks


def get_available_tasks_for_user(user_id: int) -> list[str]:
    available_tasks = []
    completed = get_completed_tasks_for_user(user_id)
    incomplete = get_incomplete_tasks_for_user(user_id)
    for exec_uuid, tasks in incomplete.items():
        for task_uuid in tasks:
            requirements = db.INJECT_REQUIREMENTS_BY_INJECT_UUID[task_uuid]
            requirement_met = 'inject_uuid' not in requirements or requirements['inject_uuid'] in completed[exec_uuid]
            if requirement_met:
                available_tasks.append(task_uuid)
    return available_tasks


def get_completion_for_users() -> dict:
    completion_per_user = {int(user_id): {} for user_id in db.USER_ID_TO_EMAIL_MAPPING.keys()}
    for exercise_status in db.EXERCISES_STATUS.values():
        for user_id in completion_per_user.keys():
            completion_per_user[int(user_id)][exercise_status['uuid']] = {}

        for task in exercise_status['tasks'].values():
            for user_id in completion_per_user.keys():
                completion_per_user[int(user_id)][exercise_status['uuid']][task['uuid']] = False
            for entry in task['completed_by_user']:
                user_id = int(entry['user_id'])
                if user_id in completion_per_user:  # Ensure the user_id is known in USER_ID_TO_EMAIL_MAPPING
                    completion_per_user[user_id][exercise_status['uuid']][task['uuid']] = entry

    return completion_per_user


def mark_task_completed(user_id: int, exercise_uuid: str , task_uuid: str):
    is_completed  = any(filter(lambda x: x['user_id'] == user_id, db.EXERCISES_STATUS[exercise_uuid]['tasks'][task_uuid]['completed_by_user']))
    if not is_completed:
        db.EXERCISES_STATUS[exercise_uuid]['tasks'][task_uuid]['completed_by_user'].append({
            'user_id': user_id,
            'timestamp': time.time(),
            'first_completion': False,
        })
    # Update who was the first to complete the task
    first_completion_index = None
    first_completion_time = time.time()
    for i, entry in enumerate(db.EXERCISES_STATUS[exercise_uuid]['tasks'][task_uuid]['completed_by_user']):
        db.EXERCISES_STATUS[exercise_uuid]['tasks'][task_uuid]['completed_by_user'][i]['first_completion'] = False
        if entry['timestamp'] < first_completion_time:
            first_completion_time = entry['timestamp']
            first_completion_index = i
    db.EXERCISES_STATUS[exercise_uuid]['tasks'][task_uuid]['completed_by_user'][first_completion_index]['first_completion'] = True


def mark_task_incomplete(user_id: int, exercise_uuid: str , task_uuid: str):
    completed_without_user = list(filter(lambda x: x['user_id'] != user_id, db.EXERCISES_STATUS[exercise_uuid]['tasks'][task_uuid]['completed_by_user']))
    db.EXERCISES_STATUS[exercise_uuid]['tasks'][task_uuid]['completed_by_user'] = completed_without_user


def get_progress():
    completion_for_users = get_completion_for_users()
    progress = {}
    selected_exercices = get_selected_exercises()
    for user_id in completion_for_users.keys():
        if user_id not in db.USER_ID_TO_EMAIL_MAPPING:
            print('unknown user id', user_id)
            continue
        progress[user_id] = {
            'email': db.USER_ID_TO_EMAIL_MAPPING[user_id],
            'user_id': user_id,
            'exercises': {},
            'status': leadboard.get_user_status(user_id, selected_exercices, get_completion_for_users())
        }
        for exec_uuid, tasks_completion in completion_for_users[user_id].items():
            if exec_uuid in selected_exercices:
                progress[user_id]['exercises'][exec_uuid] = {
                    'tasks_completion': tasks_completion,
                    'score': leadboard.get_score_for_task_completion(tasks_completion),
                    'max_score': db.EXERCISES_STATUS[exec_uuid]['max_score'],
                }
    return progress


def get_users_stats() -> dict:
    selected_exercices = get_selected_exercises()
    completion_for_users = get_completion_for_users()
    return leadboard.get_user_stats(selected_exercices, completion_for_users)


@debounce_check_active_tasks(debounce_seconds=2)
async def check_active_tasks_debounced(user_id: int, data: dict, context: dict, for_target_tool: Union[str, None] = None) -> bool:
    return await check_active_tasks(user_id, data, context, for_target_tool)


async def check_active_tasks(user_id: int, data: dict, context: dict, for_target_tool: Union[str, None] = None) -> bool:
    succeeded_once = False
    available_tasks = get_available_tasks_for_user(user_id)
    for task_uuid in available_tasks:
        inject = db.INJECT_BY_UUID[task_uuid]
        if inject['exercise_uuid'] not in db.SELECTED_EXERCISES:
            continue
        logger.debug(f"[{task_uuid}] :: checking: {inject['name']}")
        completed = await check_inject(user_id, inject, data, context, for_target_tool)
        if completed:
            succeeded_once = True
    return succeeded_once


async def check_inject(user_id: int, inject: dict, data: dict, context: dict, for_target_tool: Union[str, None] = None) -> bool:
    from backend.server import sendUserInjectCheckInProgress

    inject_evaluation_join_type = inject.get('inject_evaluation_join_type', 'UNDEFINED')
    for_target_tool = for_target_tool if for_target_tool is not None else inject['target_tool']
    if inject['target_tool'] == 'MISP' and inject['target_tool'] == for_target_tool:
        inject_checker_router = inject_checker_router_misp
    elif inject['target_tool'] == 'suricata' and inject['target_tool'] == for_target_tool:
        inject_checker_router = inject_checker_router_suricata
    elif inject['target_tool'] == 'webhook' and inject['target_tool'] == for_target_tool:
        inject_checker_router = inject_checker_router_webhook
    else:
        return False

    successCount = 0
    for inject_evaluation in inject['inject_evaluation']:
        await sendUserInjectCheckInProgress(user_id, inject['uuid'])
        success = await inject_checker_router(user_id, inject_evaluation, data, context)
        if not success and inject_evaluation_join_type == 'AND':
            logger.info(f"Task not completed[{user_id}]: {inject['uuid']}. failure of one inject and join type is `AND`")
            return False
        elif success:
            successCount += 1
            if inject_evaluation_join_type == 'OR':
                mark_task_completed(user_id, inject['exercise_uuid'], inject['uuid'])
                logger.info(f"Task success[{user_id}]: {inject['uuid']}")
                return True
            elif successCount == len(inject['inject_evaluation']):
                mark_task_completed(user_id, inject['exercise_uuid'], inject['uuid'])
                logger.info(f"Task success[{user_id}]: {inject['uuid']}")
                return True
    logger.info(f"Task not completed[{user_id}]: {inject['uuid']}. failure of all injects")
    return False


async def check_inject_for_timed_inject(inject: dict, data: dict, context: dict) -> bool:
    from backend.server import sendUserInjectCheckInProgress

    inject_evaluation_join_type = inject.get('inject_evaluation_join_type', 'UNDEFINED')
    if inject['target_tool'] == 'MISP':
        inject_checker_router = inject_checker_router_misp
    elif inject['target_tool'] == 'suricata':
        inject_checker_router = inject_checker_router_suricata
    elif inject["target_tool"] == "webhook":
        inject_checker_router = inject_checker_router_webhook
    else:
        return False

    at_last_one_success = False
    for user_id in db.USER_ID_TO_EMAIL_MAPPING.keys():

        if not is_user_email_known(user_id):
            logger.info(f"User[{user_id}] email is not unknown.")
            continue

        fullContext = dict(context)
        fullContext['user_id'] = user_id
        fullContext['user_email'] = db.USER_ID_TO_EMAIL_MAPPING.get(user_id, None)
        fullContext['user_authkey'] = db.USER_ID_TO_AUTHKEY_MAPPING.get(user_id, None)

        successCount = 0
        completed = False
        available_tasks = get_available_tasks_for_user(user_id)
        if inject['uuid'] not in available_tasks:
            continue

        for inject_evaluation in inject['inject_evaluation']:

            if inject_evaluation['evaluation_strategy'] != 'query_search':
                if inject_evaluation_join_type == 'AND':
                    logger.info(f"Unsupported evaluation_strategy `{inject_evaluation['evaluation_strategy']}` and evaluation join type `{inject_evaluation_join_type}` for Timed inject")
                    break
                elif inject_evaluation_join_type == 'OR':
                    continue

            await sendUserInjectCheckInProgress(user_id, inject['uuid'])
            success = await inject_checker_router(user_id, inject_evaluation, data, fullContext)
            if not success and inject_evaluation_join_type == 'AND':
                mark_task_completed(user_id, inject['exercise_uuid'], inject['uuid'])
                logger.info(f"Task success[{user_id}]: {inject['uuid']}")
                completed = True
                break
            elif success:
                successCount += 1
                if inject_evaluation_join_type == 'OR':
                    mark_task_completed(user_id, inject['exercise_uuid'], inject['uuid'])
                    logger.info(f"Task success[{user_id}]: {inject['uuid']}")
                    completed = True
                    break
                elif successCount == len(inject['inject_evaluation']):
                    mark_task_completed(user_id, inject['exercise_uuid'], inject['uuid'])
                    logger.info(f"Task success[{user_id}]: {inject['uuid']}")
                    completed = True
                    break
        if not completed:
            logger.info(f"Task not completed[{user_id}]: {inject['uuid']}. failure of all injects")
        else:
            at_last_one_success = True
    return at_last_one_success
