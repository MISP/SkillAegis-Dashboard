#!/usr/bin/env python3

from collections import defaultdict
from pathlib import Path
import json
import re
from typing import Union
import db
from inject_evaluator import eval_data_filtering, eval_query_comparison
import misp_api
import config

ACTIVE_EXERCISES_DIR = "active_exercises"


def load_exercises() -> bool:
    db.ALL_EXERCISES = read_exercise_dir()
    init_inject_flow()
    init_exercises_tasks()
    return True


def read_exercise_dir():
    script_dir = Path(__file__).parent
    target_dir = script_dir / ACTIVE_EXERCISES_DIR
    json_files = target_dir.glob("*.json")
    exercises = []
    for json_file in json_files:
        with open(json_file) as f:
            parsed_exercise = json.load(f)
            exercises.append(parsed_exercise)
    return exercises


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
            tasks.append(
                {
                    "name": inject['name'],
                    "uuid": inject['uuid'],
                    "score": score,
                }
            )
        exercises.append(
            {
                "name": exercise['exercise']['name'],
                "uuid": exercise['exercise']['uuid'],
                "description": exercise['exercise']['description'],
                "level": exercise['exercise']['meta']['level'],
                "priority": exercise['exercise']['meta'].get('priority', 50),
                "tasks": tasks,
            }
        )
    exercises = sorted(exercises, key=lambda d: d['priority'])
    return exercises


def get_selected_exercises():
    return db.SELECTED_EXERCISES


def change_exercise_selection(exercise_uuid: str, selected: bool):
    if selected:
        if exercise_uuid not in db.SELECTED_EXERCISES:
            db.SELECTED_EXERCISES.append(exercise_uuid)
    else:
        if exercise_uuid in db.SELECTED_EXERCISES:
            db.SELECTED_EXERCISES.remove(exercise_uuid)


def resetAllExerciseProgress():
    for user_id in db.USER_ID_TO_EMAIL_MAPPING.keys():
        for exercise_status in db.EXERCISES_STATUS.values():
            for task in exercise_status['tasks'].values():
                mark_task_incomplete(user_id, exercise_status['uuid'], task['uuid'])


def get_completed_tasks_for_user(user_id: int):
    completion = get_completion_for_users()[user_id]
    completed_tasks = {}
    for exec_uuid, tasks in completion.items():
        completed_tasks[exec_uuid] = [task_uuid for task_uuid, completed in tasks.items() if completed]
    return completed_tasks

def get_incomplete_tasks_for_user(user_id: int):
    completion = get_completion_for_users()[user_id]
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


def get_model_action(data: dict):
    if 'Log' in data:
        data = data['Log']
        if 'model' in data and 'action' in data:
            return (data['model'], data['action'],)
    return (None, None,)

def is_accepted_query(data: dict) -> bool:
    model, action = get_model_action(data)
    if model in ['Event', 'Attribute', 'Object', 'Tag',]:
        if action in ['add', 'edit', 'delete', 'publish']:
            # # improved condition below. It blocks some queries
            # if data['Log']['change'].startswith('attribute_count'):
            #     return False
            if data['Log']['change'].startswith('Validation errors:'):
                return False
            return True

    if data.get('user_agent', None) == 'misp-exercise-dashboard':
        return None
    url = data.get('url', None)
    if url is not None:
        return url in [
            '/attributes/restSearch',
            '/events/restSearch',
        ]
    return False


def get_completion_for_users():
    completion_per_user = {int(user_id): {} for user_id in db.USER_ID_TO_EMAIL_MAPPING.keys()}
    for exercise_status in db.EXERCISES_STATUS.values():
        for user_id in completion_per_user.keys():
            completion_per_user[int(user_id)][exercise_status['uuid']] = {}

        for task in exercise_status['tasks'].values():
            for user_id in completion_per_user.keys():
                completion_per_user[int(user_id)][exercise_status['uuid']][task['uuid']] = False
            for user_id in task['completed_by_user']:
                completion_per_user[int(user_id)][exercise_status['uuid']][task['uuid']] = True

    return completion_per_user


def get_score_for_task_completion(tasks_completion: dict) -> int:
    score = 0
    for inject_uuid, completed in tasks_completion.items():
        if not completed:
            continue
        inject = db.INJECT_BY_UUID[inject_uuid]
        try:
            for inject_eval in inject['inject_evaluation']:
                score += inject_eval['score_range'][1]
        except KeyError:
            pass
    return score


def mark_task_completed(user_id: int, exercise_uuid: str , task_uuid: str):
    if user_id not in db.EXERCISES_STATUS[exercise_uuid]['tasks'][task_uuid]['completed_by_user']:
        db.EXERCISES_STATUS[exercise_uuid]['tasks'][task_uuid]['completed_by_user'].append(user_id)


def mark_task_incomplete(user_id: int, exercise_uuid: str , task_uuid: str):
    if user_id in db.EXERCISES_STATUS[exercise_uuid]['tasks'][task_uuid]['completed_by_user']:
        db.EXERCISES_STATUS[exercise_uuid]['tasks'][task_uuid]['completed_by_user'].remove(user_id)


def get_progress():
    completion_for_users = get_completion_for_users()
    progress = {}
    for user_id in completion_for_users:
        progress[user_id] = {
            'email': db.USER_ID_TO_EMAIL_MAPPING[user_id],
            'exercises': {},
        }
        for exec_uuid, tasks_completion in completion_for_users[user_id].items():
            progress[user_id]['exercises'][exec_uuid] = {
                'tasks_completion': tasks_completion,
                'score': get_score_for_task_completion(tasks_completion),
                'max_score': db.EXERCISES_STATUS[exec_uuid]['max_score'],
            }
    return progress


def check_inject(user_id: int, inject: dict, data: dict, context: dict) -> bool:
    for inject_evaluation in inject['inject_evaluation']:
        success = inject_checker_router(user_id, inject_evaluation, data, context)
        if not success:
            return False
    mark_task_completed(user_id, inject['exercise_uuid'], inject['uuid'])
    print(f'Task success: {inject['uuid']}')
    return True


def is_valid_evaluation_context(user_id: int, inject_evaluation: dict, data: dict, context: dict) -> bool:
    if 'evaluation_context' not in inject_evaluation or len(inject_evaluation['evaluation_context']) == 0:
        return True
    if 'request_is_rest' in inject_evaluation['evaluation_context']:
        if 'request_is_rest' in context:
            if inject_evaluation['evaluation_context']['request_is_rest'] == context['request_is_rest']:
                return True
            else:
                print('Request type does not match state of `request_is_rest`')
                return False
        else:
            print('Unknown request type')
            return False
    return False

def inject_checker_router(user_id: int, inject_evaluation: dict, data: dict, context: dict) -> bool:
    if not is_valid_evaluation_context(user_id, inject_evaluation, data, context):
        return False

    if 'evaluation_strategy' not in inject_evaluation:
        return False

    data_to_validate = get_data_to_validate(user_id, inject_evaluation, data)
    if data_to_validate is None:
        print('Could not fetch data to validate')
        return False

    if inject_evaluation['evaluation_strategy'] == 'data_filtering':
        return eval_data_filtering(user_id, inject_evaluation, data_to_validate)
    elif inject_evaluation['evaluation_strategy'] == 'query_comparison':
        expected_data = data_to_validate['expected_data']
        data_to_validate = data_to_validate['data_to_validate']
        return eval_query_comparison(user_id, expected_data, data_to_validate)
    return False


def get_data_to_validate(user_id: int, inject_evaluation: dict, data: dict) -> Union[dict, list, str, None]:
    data_to_validate = None
    if inject_evaluation['evaluation_strategy'] == 'data_filtering':
        event_id = parse_event_id_from_log(data)
        data_to_validate = fetch_data_for_data_filtering(event_id=event_id)
    elif inject_evaluation['evaluation_strategy'] == 'query_comparison':
        perfomed_query = parse_performed_query_from_log(data)
        data_to_validate = fetch_data_for_query_comparison(user_id, inject_evaluation, perfomed_query)
    return data_to_validate


def parse_event_id_from_log(data: dict) -> Union[int, None]:
    event_id_from_change_field_regex = r".*event_id \(.*\) => \((\d+)\).*"
    event_id_from_title_field_regex = r".*from Event \((\d+)\).*"
    if 'Log' in data:
        log = data['Log']
        if 'model' in log and 'model_id' in log and log['model'] == 'Event':
            return int(log['model_id'])
        if 'change' in log:
            event_id_search = re.search(event_id_from_change_field_regex, log['change'], re.IGNORECASE)
            if event_id_search is not None:
                event_id = event_id_search.group(1)
                return event_id
        if 'title' in log:
            event_id_search = re.search(event_id_from_title_field_regex, log['title'], re.IGNORECASE)
            if event_id_search is not None:
                event_id = event_id_search.group(1)
                return event_id
    return None


def parse_performed_query_from_log(data: dict) -> Union[dict, None]:
    performed_query = {
        'request_method': '',
        'url': '',
        'payload': {},
    }
    if 'request' in data:
        request = data['request']
        performed_query['request_method'] = data.get('request_method', None)
        performed_query['url'] = data.get('url', None)
        if request.startswith('application/json\n\n'):
            query_raw = request.replace('application/json\n\n', '')
            try:
                payload = json.loads(query_raw)
                performed_query['payload'] = payload
            except:
                pass
        if performed_query['request_method'] is not None and performed_query['url'] is not None:
            return performed_query 
    return None


def fetch_data_for_data_filtering(event_id=None) -> Union[None, dict]:
    data = None
    if event_id is not None:
        data = misp_api.getEvent(event_id)
    return data


def fetch_data_for_query_comparison(user_id: int, inject_evaluation: dict, perfomed_query: dict) -> Union[None, dict]:
    data = None
    authkey = db.USER_ID_TO_AUTHKEY_MAPPING[user_id]
    if perfomed_query is not None:
        if 'evaluation_context' not in inject_evaluation and 'query_context' not in inject_evaluation['evaluation_context']:
            return None
        query_context = inject_evaluation['evaluation_context']['query_context']
        expected_method = query_context['request_method']
        expected_url = query_context['url']
        expected_payload = inject_evaluation['parameters'][0]
        expected_data  = misp_api.doRestQuery(authkey, expected_method, expected_url, expected_payload)
        data_to_validate  = misp_api.doRestQuery(authkey, perfomed_query['request_method'], perfomed_query['url'], perfomed_query['payload'])
        data = {
            'expected_data' : expected_data,
            'data_to_validate' : data_to_validate,
        }
    return data


def check_active_tasks(user_id: int, data: dict, context: dict) -> bool:
    succeeded_once = False
    available_tasks = get_available_tasks_for_user(user_id)
    for task_uuid in available_tasks:
        inject = db.INJECT_BY_UUID[task_uuid]
        if inject['exercise_uuid'] not in db.SELECTED_EXERCISES:
            print(f'exercise not active for this inject {inject['name']}')
            continue
        print(f'checking: {inject['name']}')
        completed = check_inject(user_id, inject, data, context)
        if completed:
            succeeded_once = True
    return succeeded_once