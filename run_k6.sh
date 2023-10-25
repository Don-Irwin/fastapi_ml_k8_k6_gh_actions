#!/bin/bash
rm -rf ./k6_results.txt
k6 run load.js --log-output file=./k6_results.txt -q
