#!/usr/bin/env python3
import epicbox

PYTHON_DOCKER_IMAGE = "python:3.13-alpine"

import json

from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class SimpleJSONHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        try:
            data = json.loads(body)
            script = data['script']
            result = doSandboxedExecution(script)
            response = {
                "status": "success" if result["exit_code"] == 0 else "failure",
                "exit_code": result["exit_code"],
                "stdout": result["stdout"].decode("utf-8"),
                "stderr": result["stderr"].decode("utf-8"),
                "duration": result["duration"],
            }

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))

        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Invalid JSON"}).encode("utf-8"))


def doSandboxedExecution(script):
    '''FIXME: Start the docker once and reuse it accross executions'''
    epicbox.configure(profiles=[epicbox.Profile("python", PYTHON_DOCKER_IMAGE)])
    files = [{"name": "main.py", "content": script.encode('utf-8')}]
    limits = {"cputime": 1, "memory": 64}
    result = epicbox.run("python", "python3 main.py", files=files, limits=limits)
    return result


port = 9573
server_address = ("", port)
httpd = HTTPServer(server_address, SimpleJSONHandler)
print(f"Starting agent on port {port}...")
httpd.serve_forever()


def setupDocker():
    pass

def teardownDocker():
    pass

def run(script):
    pass
