#!/bin/bash

DEFAULT_HOST="127.0.0.1"
DEFAULT_PORT="4001"

usage() {
    echo "Usage: $0 --exercise_folder <folder> [--host <host>] [--port <port>]"
    exit 1
}

HOST="${SKILLAEGIS_HOST:-""}"
PORT="${SKILLAEGIS_PORT:-""}"
EXERCISE_FOLDER="${SKILLAEGIS_EXERCISE_FOLDER:-""}"

while [ "$#" -gt 0 ]; do
    case "$1" in
        --host)
            HOST="$2"
            shift 2
            ;;
        --port)
            PORT="$2"
            shift 2
            ;;
        --exercise_folder)
            EXERCISE_FOLDER="$2"
            shift 2
            ;;
        *)
            usage
            ;;
    esac
done

if [ -z "$EXERCISE_FOLDER" ]; then
    echo "Error: --exercise_folder value is required."
    usage
fi

HOST=${HOST:-$DEFAULT_HOST}
PORT=${PORT:-$DEFAULT_PORT}

source venv/bin/activate
python3 server.py --host "$HOST" --port "$PORT" --exercise_folder "$EXERCISE_FOLDER"
