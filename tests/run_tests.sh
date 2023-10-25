rm -rf __pycache__
export REDIS_SERVER=localhost
poetry run pytest -vv -s
