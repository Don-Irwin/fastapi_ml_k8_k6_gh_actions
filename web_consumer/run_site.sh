#!/bin/bash

# conda deactivate
# deactivate

#clear out any pycache folders 
find . -type d -name __pycache__ -exec rm -r {} \+

. setup_venv.sh

#not yet needed.
#python create_db.py


echo "*********************************"
echo "*                               *"
echo "*  KILLING ANY PROCESS          *"
echo "*  Using Port 5023              *"
echo "*                               *"
echo "*********************************"

pid_to_kill=$(lsof -t -i :5023 -s TCP:LISTEN)

echo "pid_to_kill=$pid_to_kill"

#Check if the variable is defined and if it has values
#and if it has values in it.
if [[ $pid_to_kill && ${pid_to_kill-_} ]]; then
  for ptk in "${pid_to_kill[@]}" ; do
      sudo kill -9 ${ptk}
  done
fi

pid_to_kill=$(lsof -t -i :5023 -s TCP:LISTEN)

echo "pid_to_kill=$pid_to_kill"

#python app.py > /dev/null &

#python app.py > /dev/null &

minikube -n w255 service frontend --url

if [ $? -ne 0 ]; then
python_api_url=$(minikube -n w255 service frontend --url)
fi


echo "python_api_url=$python_api_url"

if [[ $python_api_url && ${python_api_url-_} ]]; then
  export ca_linear_model_api_url=$python_api_url
fi


#python app.py

nohup python app.py &

flask_app_pid=$!


echo "*********************************"
echo "*                               *"
echo "*   Waiting for flask to        *"
echo "*      spin up                  *"
echo "*                               *"
echo "*********************************"


finished=false
while ! $finished; do
    health_status=$(curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://127.0.0.1:5023")
    if [ $health_status == "200" ]; then
        finished=true
        echo "*********************************"
        echo "*                               *"
        echo "*        Flask is ready         *"
        echo "*                               *"
        echo "*********************************"
    else
        finished=false
    fi
done

echo "***********************************"
echo "*                                 *"
echo "* Access Flask at the following   *"
echo "* Address                         *"
echo "* http://127.0.0.1:5023           *"
echo "*                                 *"
echo "***********************************"
echo ""
echo "*********************************"
echo "*                               *"
echo "*   Press enter to kill the     *"
echo "*      Flask application        *"
echo "*                               *"
echo "*********************************"


read -p "Press enter to kill flask application:\n"

sudo kill ${flask_app_pid}

conda deactivate
deactivate

rm -rf w210_web

