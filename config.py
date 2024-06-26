
misp_url = 'https://localhost/'
misp_apikey = 'FI4gCRghRZvLVjlLPLTFZ852x2njkkgPSz0zQ3E0'
misp_skipssl = True

live_logs_accepted_scope = {
    'rest_client_history': '*',
    'events': ['add', 'edit', 'delete', 'restSearch',],
    'attributes': ['add', 'edit', 'delete', 'restSearch',],
    'tags': '*',
}