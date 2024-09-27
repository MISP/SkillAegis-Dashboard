#!/bin/bash

DEFAULT_HOST="127.0.0.1"
DEFAULT_PORT="4001"

usage() {
    echo "Usage: $0 --exercise_folder <folder> [--host <host>] [--port <port>] [--misp_url <misp_url>] [--misp_apikey <misp_apikey>] [--misp_skipssl <misp_skipssl>]"
    exit 1
}

HOST="${SKILLAEGIS_HOST:-""}"
PORT="${SKILLAEGIS_PORT:-""}"
EXERCISE_FOLDER="${SKILLAEGIS_EXERCISE_FOLDER:-""}"
MISP_URL="${SKILLAEGIS_MISP_URL:-""}"
MISP_APIKEY="${SKILLAEGIS_MISP_APIKEY:-""}"
MISP_SKIPSSL="${SKILLAEGIS_MISP_SKIPSSL:-""}"

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
        --misp_url)
            MISP_URL="$2"
            shift 2
            ;;
        --misp_apikey)
            MISP_APIKEY="$2"
            shift 2
            ;;
        --misp_skipssl)
            MISP_SKIPSSL="$2"
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
python3 ./backend/main.py \
    --host "$HOST" --port "$PORT" \
    --exercise_folder "$EXERCISE_FOLDER" \
    --misp_url "$MISP_URL" \
    --misp_apikey "$MISP_APIKEY" \
    --misp_skipssl "$MISP_SKIPSSL"
