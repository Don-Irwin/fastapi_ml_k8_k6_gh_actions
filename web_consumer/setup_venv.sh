#!/bin/bash
source ./env.sh
rm -rf ./${VENV_NAME}
python3 -m venv ${VENV_NAME}
source ./${VENV_NAME}/bin/activate
. ir.sh


#pip install git+https://github.com/b3mery/AmortaPy.git
