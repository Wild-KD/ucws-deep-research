#!/bin/bash
# Start the Investment Research Engine
cd "$(dirname "$0")"
exec uvicorn server:app --host 0.0.0.0 --port ${PORT:-9001}
