#!/bin/bash

export REDIS_SERVER=localhost
echo $REDIS_SERVER

poetry run uvicorn main:app --reload
