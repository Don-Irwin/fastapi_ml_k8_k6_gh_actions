#!/bin/bash
echo "kubectl delete -f deployment-pythonapi.yaml"
kubectl delete -f deployment-pythonapi.yaml
echo "kubectl delete -f deployment-pythonapi-consumer.yaml"
kubectl delete -f deployment-pythonapi-consumer.yaml
echo "kubectl delete -f deployment-redis.yaml"
kubectl delete -f deployment-redis.yaml
echo "kubectl delete -f service-redis.yaml"
kubectl delete -f service-redis.yaml
echo "kubectl delete -f service-prediction-consumer.yaml"
kubectl delete -f service-prediction-consumer.yaml
echo "kubectl delete -f service-prediction.yaml"
kubectl delete -f service-prediction.yaml
echo "kubectl delete -f service-prediction_a.yaml"
kubectl delete -f service-prediction_a.yaml
echo "kubectl delete -f istio-gateway-prediction.yaml"
kubectl delete -f istio-gateway-prediction.yaml
echo "kubectl delete -f namespace.yaml"
kubectl delete -f namespace.yaml
echo "kubectl delete -f prediction-grafana.yaml"
kubectl delete -f prediction-grafana.yaml
echo "kubectl delete -f telemetry.yaml"
kubectl delete -f telemetry.yaml

#inject prometheus
#https://istio.io/latest/docs/ops/integrations/prometheus/
kubectl delete -f https://raw.githubusercontent.com/istio/istio/release-1.19/samples/addons/prometheus.yaml

#inject grafana;
#https://istio.io/latest/docs/ops/integrations/grafana/
kubectl delete -f https://raw.githubusercontent.com/istio/istio/release-1.19/samples/addons/grafana.yaml
