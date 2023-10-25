#!/bin/bash
cd /lab1
poetry install --no-dev
export PATH="/lab1/venv/bin:$PATH"
python -m venv --copies ./venv
chmod -R 777 ./*.*
. ./venv/bin/activate && poetry install --no-dev
