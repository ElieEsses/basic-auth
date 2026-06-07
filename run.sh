#!/usr/bin/env bash
set -e

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m Project.main
