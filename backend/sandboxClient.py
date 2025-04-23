#!/usr/bin/env python3


import json
import http.client
from typing import Union

headers = {"Content-Type": "application/json"}
port = 9573

VALIDATION_TRUE = "__validation_true__"
VALIDATION_FALSE = "__validation_false__"


def run(inject_evaluation: dict, data: dict, context: dict, debug: bool = False) -> Union[bool, tuple]:
    context_for_script = {
        'data': data,
        'context': context,
    }
    evaluation_params = inject_evaluation["parameters"]
    evaluation_script = evaluation_params[0]
    lines = evaluation_script.splitlines()
    indentedLines = [f"    {l}" for l in lines]
    indentedScript = "\n".join(indentedLines)
    data_str = json.dumps(data)
    context_str = json.dumps(context_for_script)
    script = f"""
import json

def evaluate(data: dict, context: dict) -> bool:
{indentedScript}

data = json.loads('{data_str}')
context = json.loads('{context_str}')
outcome = evaluate(data, context)
if outcome is True:
    print('{VALIDATION_TRUE}')
else:
    print('{VALIDATION_FALSE}')
"""
    result = sendScriptToAgent(script, context)
    eval_returned_true = VALIDATION_TRUE in result["stdout"]
    result["stdout"] = result["stdout"].replace(VALIDATION_TRUE, '').replace(VALIDATION_FALSE, '')

    if debug:
        if result['status'] == 'success':
            return (True, [[result]],) if eval_returned_true else (False, [[result]],)
        return (False, [[result]],)
    else:
        if result['status'] == 'success':
            return eval_returned_true
        return False


def sendScriptToAgent(script, context) -> dict:
    conn = http.client.HTTPConnection("localhost", port)
    payload = {"script": script, "context": context}
    conn.request("POST", "/", body=json.dumps(payload), headers=headers)

    response = conn.getresponse()
    result = json.loads(response.read().decode())
    conn.close()
    return result
