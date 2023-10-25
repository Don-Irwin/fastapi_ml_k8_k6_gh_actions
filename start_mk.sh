#!/bin/bash
time minikube start --kubernetes-version=v1.25.13 --memory 16384 --cpus 4  --force
eval $(minikube -p minikube docker-env)
istioctl install --set profile=demo -y
IMAGE_NAME=w255_lab3_don_irwin
#minikube image load ${IMAGE_NAME}