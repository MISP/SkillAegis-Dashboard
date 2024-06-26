#!/usr/bin/env python3
from typing import Union
import jq
import re
import operator


def jq_extract(path: str, data: dict):
    path = '.' + path if not path.startswith('.') else path
    return jq.compile(path).input_value(data).first()


##
## Data Filtering
##

def condition_satisfied(evaluation_config: dict, data_to_validate: Union[dict, list, str]) -> bool:
    if type(data_to_validate) is str:
        return eval_condition_str(evaluation_config, data_to_validate)
    elif type(data_to_validate) is list:
        return eval_condition_list(evaluation_config, data_to_validate)
    elif type(data_to_validate) is dict:
        # Not sure how we could have condition on this
        return eval_condition_dict(evaluation_config, data_to_validate)
    return False


def eval_condition_str(evaluation_config: dict, data_to_validate: str) -> bool:
    comparison_type = evaluation_config['comparison']
    values = evaluation_config['values']
    if len(values) == 0:
        return False

    if comparison_type == 'contains':
        values = [v.lower() for v in values]
        data_to_validate = data_to_validate.lower()
        data_to_validate_set = set(data_to_validate.split())
        values_set = set(values)
        intersection = data_to_validate_set & values_set
        return len(intersection) == len(values_set)
    elif comparison_type == 'equals':
        return data_to_validate == values[0]
    elif comparison_type == 'regex':
        return re.fullmatch(values[0], data_to_validate)
    elif comparison_type == 'count':
        return len(data_to_validate) == values[0]
    return False


def eval_condition_list(evaluation_config: dict, data_to_validate: str) -> bool:
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

    data_to_validate_set = set(data_to_validate)
    values_set = set(values)

    if comparison_type == 'contains':
        intersection = data_to_validate_set & values_set
        return len(intersection) == len(values_set)
    elif comparison_type == 'equals':
        intersection = data_to_validate_set & values_set
        return len(intersection) == len(values_set) and len(intersection) == len(data_to_validate_set)
    elif comparison_type == 'count':
        if values[0].isdigit():
            return len(data_to_validate) == values[0]
        elif values[0][0] in comparators.keys():
            count = len(data_to_validate)
            value_operator = values[0][0]
            value = int(values[0][1:])
            return comparators[value_operator](count, value)
    return False


def eval_condition_dict(evaluation_config: dict, data_to_validate: str) -> bool:
    print('Condition on dict not supported yet')
    comparison_type = evaluation_config['comparison']
    if comparison_type == 'contains':
        pass
    elif comparison_type == 'equals':
        pass
    elif comparison_type == 'count':
        pass
    return False


def eval_data_filtering(user_id: int, inject_evaluation: dict, data: dict) -> bool:
    for evaluation_params in inject_evaluation['parameters']:
        for evaluation_path, evaluation_config in evaluation_params.items():
            data_to_validate = jq_extract(evaluation_path, data)
            if data_to_validate is None:
                return False
            if not condition_satisfied(evaluation_config, data_to_validate):
                return False
    return True


##
## Query comparison
##

def eval_query_comparison(user_id: int, expected_data, data_to_validate) -> bool:
    return expected_data == data_to_validate
