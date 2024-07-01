
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