
server_host = '0.0.0.0'
server_port = 4000
zmq_url = 'tcp://localhost:50000'

misp_url = 'https://localhost/'
misp_apikey = 'FI4gCRghRZvLVjlLPLTFZ852x2njkkgPSz0zQ3E0'
misp_skipssl = True

live_logs_accepted_scope = {
    'events': ['add', 'edit', 'delete', 'restSearch',],
    'attributes': ['add', 'edit', 'delete', 'restSearch',],
    'tags': '*',
}

import logging
logger = logging.getLogger('misp-exercise-dashboard')
format = '[%(levelname)s] %(asctime)s - %(message)s'
formatter = logging.Formatter(format)
logging.basicConfig(filename='misp-exercise-dashboard.log', encoding='utf-8', level=logging.DEBUG, format=format)
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
logger.addHandler(ch)
