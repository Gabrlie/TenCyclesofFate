#!/bin/bash
# This script starts the FastAPI application using the correct Uvicorn syntax.

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Load environment variables from .env file if it exists
# 优先从根目录加载，然后是 backend 目录
if [ -f .env ]; then
  echo "Loading environment from .env"
  # Convert CRLF to LF for cross-platform compatibility
  sed -i 's/\r$//' .env 2>/dev/null || sed -i '' 's/\r$//' .env 2>/dev/null
  # Using a safer method to export variables
  set -o allexport
  source .env
  set +o allexport
elif [ -f backend/.env ]; then
  echo "Loading environment from backend/.env"
  sed -i 's/\r$//' backend/.env 2>/dev/null || sed -i '' 's/\r$//' backend/.env 2>/dev/null
  set -o allexport
  source backend/.env
  set +o allexport
else
  echo "Warning: No .env file found. Using default values."
fi

# Use environment variables for host and port, with defaults
HOST=${HOST:-"0.0.0.0"}
PORT=${PORT:-8000}

RELOAD_FLAG=""
# Check for 'true' in a case-insensitive way
if [[ "${UVICORN_RELOAD,,}" == "true" ]]; then
    RELOAD_FLAG="--reload"
fi

echo "Attempting to start server on ${HOST}:${PORT} with reload flag: '${RELOAD_FLAG}'"

# The command 'uv run uvicorn' is equivalent to 'uv uvicorn'.
# The key is the 'backend.app.main:app' part, which specifies the app instance.
python -m uvicorn backend.app.main:app --host ${HOST} --port ${PORT} ${RELOAD_FLAG}