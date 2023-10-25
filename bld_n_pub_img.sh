#!/bin/bash
IMAGE_NAME=w255_lab3_don_irwin_enhanced
APP_NAME=w255_lab3_don_irwin_enhanced
DOCKER_FILE=Dockerfile.255lab3
DOCKER_REPO=donirwinberkeley
#make sure minikube is down
minikube stop
#re-eval so it bulds locally
eval $(minikube docker-env -u)
#build the image to local docker
time docker build -t ${IMAGE_NAME} -f ${DOCKER_FILE} .
docker login
docker tag ${IMAGE_NAME} ${DOCKER_REPO}/${IMAGE_NAME}:x86_latest
docker push ${DOCKER_REPO}/${IMAGE_NAME}:x86_latest
