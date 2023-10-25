#!/bin/bash
source ./env.sh

#get these values from the env bash file
# IMAGE_NAME_WC=w255_l3_api_web_consumer
# APP_NAME_WC=w255_l3_api_web_consumer
# DOCKER_FILE_WC=Dockerfile.api_consumer



find . -type d -name __pycache__ -exec rm -r {} \+
deactivate
rm -rf ./${VENV_NAME}

#docker rmi $(docker images --filter "dangling=true" -q --no-trunc)

echo "docker stop ${APP_NAME_WC}"
docker stop ${APP_NAME_WC}
echo "docker rm ${APP_NAME_WC}"
docker rm ${APP_NAME_WC}

#build docker from the docker file
echo "docker build -t ${IMAGE_NAME_WC} -f ${DOCKER_FILE_WC}" 
docker build -t ${IMAGE_NAME_WC} -f ${DOCKER_FILE_WC} .


