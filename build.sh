#!/bin/bash
set -e

VENV_PIP="venv/bin/pip"


pip install --upgrade pip
pip install -r requirements.txt

docker build -t flowio-pptx1-prod .

echo "Build complete."

