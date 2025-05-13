#!/usr/bin/env python3

import epicbox

PYTHON_DOCKER_IMAGE = "python:3.13-alpine"

from http.server import BaseHTTPRequestHandler, HTTPServer
import json


sandbox = None
epicbox.configure(profiles=[epicbox.Profile("python", PYTHON_DOCKER_IMAGE)])
sandbox_limits = {"cputime": 1, "memory": 64}


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
    global sandbox
    files = [{"name": "main.py", "content": script.encode("utf-8")}]
    epicbox.sandboxes._write_files(sandbox.container, files)
    result = epicbox.start(sandbox)
    return result

def startAgent():
    port = 9573
    server_address = ("", port)
    httpd = HTTPServer(server_address, SimpleJSONHandler)
    httpd.serve_forever()


if __name__ == '__main__':
    with epicbox.create('python', command="python3 main.py", limits=sandbox_limits) as agentSandbox:
        sandbox = agentSandbox
        startAgent()
