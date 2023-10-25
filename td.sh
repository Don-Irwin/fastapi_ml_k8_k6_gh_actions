#!/bin/bash

echo "*********************************"
echo "*  KILLING                      *"
echo "* Docker stopping and remove    *"
echo "*                               *"
echo "* Stopping Kubernetes           *"
echo "*                               *"
echo "*********************************"

IMAGE_NAME=w255_lab3_don_irwin
APP_NAME=w255_lab3_don_irwin
DOCKER_FILE=Dockerfile.255lab3


echo "docker stop ${APP_NAME}"
docker stop ${APP_NAME}
echo "docker rm ${APP_NAME}"
docker rm ${APP_NAME}
cd ./infra
. delete_deployments.sh
cd ./../
minikube stop



kill $proxy_pid
kill $port_forwarding_pid

