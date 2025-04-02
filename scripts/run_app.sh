#!/bin/bash

# Always start from project root
cd "$(dirname "$0")"/..

# Add src/ to PYTHONPATH
export PYTHONPATH="$(pwd)/src"

echo "Run the application"
python src/gui/tkinter_app.py
