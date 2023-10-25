#!/bin/bash

#inject prometheus
#https://istio.io/latest/docs/ops/integrations/prometheus/
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.19/samples/addons/prometheus.yaml

#inject grafana;
#https://istio.io/latest/docs/ops/integrations/grafana/
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.19/samples/addons/grafana.yaml


echo "kubectl create -f namespace.yaml"
kubectl create -f namespace.yaml
echo "kubectl apply -f deployment-redis.yaml"
kubectl apply -f deployment-redis.yaml
echo "kubectl apply -f service-redis.yaml"
kubectl apply -f service-redis.yaml
echo "kubectl apply -f deployment-pythonapi.yaml"
kubectl apply -f deployment-pythonapi.yaml
echo "kubectl apply -f deployment-pythonapi-consumer.yaml"
kubectl apply -f deployment-pythonapi-consumer.yaml
echo "kubectl apply -f service-prediction.yaml"
kubectl apply -f service-prediction.yaml
echo "kubectl apply -f service-prediction-consumer.yaml"
kubectl apply -f service-prediction-consumer.yaml
echo "kubectl apply -f service-prediction_a.yaml"
kubectl apply -f service-prediction_a.yaml
echo "kubectl apply -f istio-gateway-prediction.yaml"
kubectl apply -f istio-gateway-prediction.yaml
echo "kubectl apply -f prediction-grafana.yaml"
kubectl apply -f prediction-grafana.yaml
echo "kubectl apply -f telemetry.yaml"
kubectl apply -f telemetry.yaml