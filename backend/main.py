#!/usr/bin/env python3

import argparse
import os
import sys
from pathlib import Path
from aiohttp import web

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import backend.config as config
import backend.exercise as exercise_model
from backend.appConfig import logger
from backend.server import init_app



def main():
    parser = argparse.ArgumentParser(description='Parse command-line arguments for SkillAegis Dashboard.')

    parser.add_argument('--host', type=str, required=False, default=config.server_host, help='The host to listen to')
    parser.add_argument('--port', type=int, required=False, default=config.server_port, help='The port to listen to')
    parser.add_argument('--exercise_folder', type=str, required=False, default=config.exercise_directory, help='The folder containing all exercises')
    parser.add_argument('--zmq_log_file', type=str, required=False, default=None, help='A ZMQ log file to replay. Will disable the ZMQ subscription defined in the settings.')
    parser.add_argument('--zmq_start_line_number', type=int, required=False, default=0, help='The line at which the ZMQ log file used for replay should start being fed.')

    args = parser.parse_args()

    # Validate exercise_folder
    if not os.path.isdir(args.exercise_folder):
        parser.error(f"The specified exercise_folder does not exist or is not a directory: {args.exercise_folder}")
    else:
        exercise_model.ACTIVE_EXERCISES_DIR = Path(args.exercise_folder)

    if args.zmq_log_file and not os.path.isfile(args.zmq_log_file):
        parser.error(f"The specified zmq_log_file does not exist or is not a file: {args.zmq_log_file}")

    exercises_loaded = exercise_model.load_exercises()
    if not exercises_loaded:
        logger.critical('Could not load exercises')
        sys.exit(1)

    web.run_app(init_app(args.zmq_log_file, args.zmq_start_line_number), host=args.host, port=args.port)


if __name__ == "__main__":
    main()
