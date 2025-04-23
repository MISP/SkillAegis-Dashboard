#!/urs/bin/env python3


from typing import Union
from backend.utils import eval_data_filtering as eval_data_filtering_util, eval_python


## Data filtering
def eval_data_filtering(user_id: int, inject_evaluation: dict, data: dict, context: dict, debug: bool = False) -> Union[bool, tuple]:
    return eval_data_filtering_util(inject_evaluation, data, context, debug = debug)


## Query mirror
def eval_query_mirror(user_id: int, expected_data, data_to_validate, context: dict) -> bool:
    return expected_data == data_to_validate


## Query search
def eval_query_search(user_id: int, inject_evaluation: dict, data: dict, context: dict, debug: bool = False) -> bool:
    return eval_data_filtering(user_id, inject_evaluation, data, context, debug = debug)

## Python
def eval_python(user_id: int, inject_evaluation: dict, data: dict, context: dict, debug: bool = False) -> bool:
    return eval_python(user_id, inject_evaluation, data, context, debug=debug)
