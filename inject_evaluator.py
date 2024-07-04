#!/usr/bin/env python3
from typing import Union
import jq
import re
import operator
from config import logger


def jq_extract(path: str, data: dict, extract_type='first'):
    query = jq.compile(path).input_value(data)
    try:
        return query.first() if extract_type == 'first' else query.all()
    except StopIteration:
        return None


# Replace the substring `{{variable}}` by context[variable] in the provided string
def apply_replacement_from_context(string: str, context: dict) -> str:
    replacement_regex = r"{{(\w+)}}"
    matches = re.fullmatch(replacement_regex, string, re.MULTILINE)
    if not matches:
        return string
    subst_str = matches.groups()[0]
    subst = str(context.get(subst_str, ''))
    return re.sub(replacement_regex, subst, string)


##
## Data Filtering
##

def condition_satisfied(evaluation_config: dict, data_to_validate: Union[dict, list, str], context: dict) -> bool:
    if type(data_to_validate) is bool:
        data_to_validate = "1" if data_to_validate else "0"
    if type(data_to_validate) is str:
        return eval_condition_str(evaluation_config, data_to_validate, context)
    elif type(data_to_validate) is list:
        return eval_condition_list(evaluation_config, data_to_validate, context)
    elif type(data_to_validate) is dict:
        # Not sure how we could have condition on this
        return eval_condition_dict(evaluation_config, data_to_validate, context)
    return False


def eval_condition_str(evaluation_config: dict, data_to_validate: str, context: dict) -> bool:
    comparison_type = evaluation_config['comparison']
    values = evaluation_config['values']
    if len(values) == 0:
        return False
    values = [apply_replacement_from_context(v, context) for v in values]

    if comparison_type == 'contains':
        values = [v.lower() for v in values]
        data_to_validate = data_to_validate.lower()
        data_to_validate_set = set(data_to_validate.split())
        values_set = set(values)
        intersection = data_to_validate_set & values_set
        return len(intersection) == len(values_set)
    elif comparison_type == 'equals':
        return data_to_validate == values[0]
    elif comparison_type == 'equals_any':
        return data_to_validate in values
    elif comparison_type == 'regex':
        return re.fullmatch(values[0], data_to_validate)
    elif comparison_type == 'count':
        return len(data_to_validate) == values[0]
    return False


def eval_condition_list(evaluation_config: dict, data_to_validate: str, context: dict) -> bool:
    comparison_type = evaluation_config['comparison']
    values = evaluation_config['values']
    comparators = {
        '<': operator.lt,
        '<=': operator.le,
        '>': operator.gt,
        '>=': operator.ge,
        '=': operator.eq,
    }

    if len(values) == 0:
        return False
    values = [apply_replacement_from_context(v, context) for v in values]

    if comparison_type == 'contains' or comparison_type == 'equals':
        data_to_validate_set = set(data_to_validate)
        values_set = set(values)
        intersection = data_to_validate_set & values_set
        if comparison_type == 'contains':
            return len(intersection) == len(values_set)
        elif comparison_type == 'equals':
            return len(intersection) == len(values_set) and len(intersection) == len(data_to_validate_set)
    if comparison_type == 'contains-regex':
        regex = re.compile(values[0])
        for candidate in data_to_validate:
            if regex.match(candidate):
                return True
        return False
    elif comparison_type == 'count':
        value = values[0]
        if value.isdigit():
            return len(data_to_validate) == value
        elif value[:2] in comparators.keys():
            count = len(data_to_validate)
            value_operator = values[0][:2]
            value = int(value[2:])
            return comparators[value_operator](count, value)
        elif value[0] in comparators.keys():
            count = len(data_to_validate)
            value_operator = value[0]
            value = int(value[1:])
            return comparators[value_operator](count, value)
    return False


def eval_condition_dict(evaluation_config: dict, data_to_validate: str, context: dict) -> bool:
    comparison_type = evaluation_config['comparison']
    values = evaluation_config['values']
    comparators = {
        '<': operator.lt,
        '<=': operator.le,
        '>': operator.gt,
        '>=': operator.ge,
        '=': operator.eq,
    }

    if len(values) == 0:
        return False
    values = [apply_replacement_from_context(v, context) for v in values]

    comparison_type = evaluation_config['comparison']
    if comparison_type == 'contains':
        pass
    elif comparison_type == 'equals':
        pass
    elif comparison_type == 'count':
        if values[0].isdigit():
            return len(data_to_validate) == values[0]
        elif values[0][0] in comparators.keys():
            count = len(data_to_validate)
            value_operator = values[0][0]
            value = int(values[0][1:])
            return comparators[value_operator](count, value)
    return False


def eval_data_filtering(user_id: int, inject_evaluation: dict, data: dict, context: dict) -> bool:
    for evaluation_params in inject_evaluation['parameters']:
        for evaluation_path, evaluation_config in evaluation_params.items():
            evaluation_path = apply_replacement_from_context(evaluation_path, context)
            data_to_validate = jq_extract(evaluation_path, data, evaluation_config.get('extract_type', 'first'))
            if data_to_validate is None:
                logger.debug('Could not extract data')
                return False
            if not condition_satisfied(evaluation_config, data_to_validate, context):
                return False
    return True


##
## Query mirror
##

def eval_query_mirror(user_id: int, expected_data, data_to_validate, context: dict) -> bool:
    return expected_data == data_to_validate



##
## Query search
##

def eval_query_search(user_id: int, inject_evaluation: dict, data: dict, context: dict) -> bool:
    return eval_data_filtering(user_id, inject_evaluation, data, context)