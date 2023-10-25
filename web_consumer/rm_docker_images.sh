#!/bin/bash
source ./env.sh

find . -type d -name __pycache__ -exec rm -r {} \+
deactivate
rm -rf ./${VENV_NAME}

echo "*********************************"
echo "  STARTING                     "
echo " Killing  ${APP_NAME_WC}       "
echo "                               "
echo "*********************************"

echo "docker stop ${APP_NAME_WC}"
docker stop ${APP_NAME_WC}
echo "docker rm ${APP_NAME_WC}"
docker rm ${APP_NAME_WC}

echo "*********************************"
echo "  STARTING                     "
echo " Finished killing  ${APP_NAME_WC}       "
echo "                               "
echo "*********************************"


