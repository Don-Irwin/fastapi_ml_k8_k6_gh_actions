#!/bin/bash
source ./env.sh
find . -type d -name __pycache__ -exec rm -r {} \+
rm -rf ./${VENV_NAME}
. build_docker.sh
docker login
docker tag ${IMAGE_NAME_WC} donirwinberkeley/${IMAGE_NAME_WC}:x86_latest
docker push donirwinberkeley/${IMAGE_NAME_WC}:x86_latest
