#!/bin/bash

kubectl port-forward -n istio-system Service/ingressgateway 8000:8000 --address='0.0.0.0' > output_$my_ticks.txt & 

echo "port-forward -n istio-system Service/grafana 3000:3000 --address='0.0.0.0' > output_$my_ticks.txt & "
kubectl port-forward -n istio-system Service/grafana 3000:3000 --address='0.0.0.0' > output_$my_ticks.txt & 



