#!/bin/bash

##NOTE: IN ORDER TO NOT WASTE BILLIONS OF HOURS BEWARE OF STARTING MINIKUBE BEFORE THE LOCAL DOCKER WORK WITH REDIS
##Very good article
##https://www.digitalocean.com/community/tutorials/how-to-install-and-use-istio-with-kubernetes
#consult:
#https://istio.io/latest/docs/setup/platform-setup/minikube/
#
#https://minikube.sigs.k8s.io/docs/handbook/accessing/
#


echo "**********************************"
echo "* U.C. Berkeley MIDS W255        *"
echo "* Summer 2022                    *"
echo "* Instructor: James York Winegar *"
echo "* Student: Don Irwin             *"
echo "* Lab 3 Submission               *"
echo "**********************************"


if [[ $W255_UP && ${W255_UP-_} ]]; then
    if [ $W255_UP -eq 1 ]; then    
        echo "**********************************"
        echo "The System is up -- exiting"
        echo "To bypass:"
        echo "export W255_UP=0"
        echo "**********************************"
    return    
    fi
fi


export REDIS_SERVER=localhost

echo "*********************************"
echo "*                               *"
echo "* CHECK DEPENDENCIES            *"
echo "*                               *"
echo "*********************************"

minikube --help>/dev/null
if [ $? -eq 0 ]; then
    echo "minikube installed"
else

    echo "*********************************"
    echo "Trying to install minikube"
    echo "https://minikube.sigs.k8s.io/docs/start/"
    echo "*********************************"
    curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
    sudo install minikube-linux-amd64 /usr/local/bin/minikube
    rm -rf ./minikube-linux-amd64



    echo "*********************************"
    echo "Trying to install minikube"
    echo "*********************************"
    minikube --help >/dev/null
    if [ $? -eq 0 ]; then
        echo "minikube is installed!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    else
        echo "*********************************"
        echo "Unable to install minikube"
        echo "*********************************"
        return
    fi

fi


kubectl --help>/dev/null

if [ $? -eq 0 ]; then
    echo "Kubectl is installed"
else

    echo "*********************************"
    echo "Trying to install kubectl"
    echo "*********************************"
    curl -LO https://dl.k8s.io/release/v1.28.1/bin/linux/amd64/kubectl
    chmod +x kubectl
    mkdir -p ~/.local/bin
    mv ./kubectl ~/.local/bin/kubectl
    echo "PATH=$PATH:~/.local/bin">>~/.bashrc
    source ~/.bashrc


    echo "*********************************"
    echo "Trying to install kubectl"
    echo "*********************************"
    kubectl --help>/dev/null
    if [ $? -eq 0 ]; then
        echo "Kubectl is installed!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    else
        echo "*********************************"
        echo "Unable to install kubectl"
        echo "*********************************"
        return
    fi

fi

istioctl --help >/dev/null

if [ $? -eq 0 ]; then
    echo "Istio is installed"
else

    echo "*********************************"
    echo "Trying to install Istio"
    echo "*********************************"
    curl -L https://istio.io/downloadIstio | ISTIO_VERSION=1.19.0 TARGET_ARCH=x86_64 sh -
    chmod +x  istio-1.19.0
    mkdir -p ~/.local/bin
    mv ./istio-1.19.0 ~/.local/bin/istio-1.19.0
    echo "PATH=$PATH:~/.local/bin/istio-1.19.0/bin">>~/.bashrc
    source ~/.bashrc


    echo "*********************************"
    echo "Trying to install Istio"
    echo "*********************************"
    istioctl --help >/dev/null
    if [ $? -eq 0 ]; then
        echo "Istio is installed!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    else
        echo "*********************************"
        echo "Unable to install Istio"
        echo "*********************************"
        return
    fi

fi


echo "*********************************"
echo "*                               *"
echo "* FINISHED                      *"
echo "* CHECK DEPENDENCIES            *"
echo "*                               *"
echo "*********************************"


#  if [ "$EUID" -ne 0 ]; then
#    echo "Please run as root"
#    return
#  fi

IMAGE_NAME=w255_lab3_don_irwin
APP_NAME=w255_lab3_don_irwin
DOCKER_FILE=Dockerfile.255lab3

echo "*********************************"
echo "*                               *"
echo "* Recycle kubernetes            *"
echo "*                               *"
echo "*********************************"

minikube stop

#VERY IMPORTANT BACK OUT YOUR MINIKUBE
#DOCKER RE-DIRECT -- OTHERWISE ALL SUBSEQUENT
#BUILDS WILL GO TO MINIKUBE -- NOT DOCKER
#wasted hours on this
eval $(minikube docker-env -u)

sleep 1

echo "*********************************"
echo "*                               *"
echo "* finished recycle k8           *"
echo "*                               *"
echo "*********************************"


echo "*********************************"
echo "*                               *"
echo "* recycle redis and create      *"
echo "*   docker network              *"
echo "*   redis outside of minicube   *"
echo "*   is needed for testing       *"
echo "*                               *"
echo "*********************************"

NET_NAME=w255
echo "docker stop redis"
docker stop redis
echo "docker rm redis"
docker rm redis

echo "docker network rm ${NET_NAME}"
docker network rm ${NET_NAME}

#echo "docker network create rm ${NET_NAME} "
#docker network create ${NET_NAME} 

sleep 2

echo "docker run -d --name redis -p 6379:6379 redis --net ${NET_NAME}"
#docker run -d --name redis -p 6379:6379 redis

#echo "docker run -d --name redis -p 6379:6379 redis --net ${NET_NAME}"
docker run -d --name redis -p 6379:6379 redis 
#echo "docker run -d -p 6379:6379 --name redis -v \"$(pwd)/redis-conf":/redis-conf redis redis-server /redis-conf"

#docker run -d -p 6379:6379 --name redis -v "$(pwd)/redis-conf":/redis-conf redis redis-server /redis-conf --net ${NET_NAME}
#return

echo "*********************************"
echo "*                               *"
echo "* Installing Dependencies       *"
echo "*   poetry install              *"
echo "*                               *"
echo "*********************************"

poetry install

echo "*********************************"
echo "*                               *"
echo "* Training the model and writing*"
echo "*   *.pkl file                  *"
echo "*                               *"
echo "*********************************"
FILE=./lab3/model_pipeline.pkl
if test -f "$FILE"; then
    echo "$FILE exists."
else
    poetry run python3 ./trainer/train.py
    cp *.pkl ./lab3/
fi

#rm *.pkl
#rm ./src/*.pkl
#poetry run python3 ./trainer/train.py

echo "*********************************"
echo "*                               *"
echo "* Copying pkl file to the src   *"
echo "*   *.pkl file                  *"
echo "*                               *"
echo "*********************************"


echo "*********************************"
echo "*                               *"
echo "* Running app locally poetry    *"
echo "*   poetry run pytest -vv -s    *"
echo "*                               *"
echo "*********************************"

poetry run pytest -vv -s
if [ $? -ne 0 ]; then

    echo "*********************************"
    echo "*  FINISHED                     *"
    echo "* Running app locally poetry    *"
    echo "*   poetry run pytest -vv -s    *"
    echo "*  FAILURE                      *"
    echo "*********************************"
    return

fi

echo "*********************************"
echo "*  FINISHED                     *"
echo "* Running app locally poetry    *"
echo "*   poetry run pytest -vv -s    *"
echo "*  SUCCESS                      *"
echo "*********************************"
#stop the image if it was running

echo "*********************************"
echo "*  STARTING                     *"
echo "* Docker stopping and rebuild   *"
echo "*                               *"
echo "*********************************"

#now that we're done with poetry, let's take down Redis
#before redirecting to minikube
NET_NAME=w255
echo "docker stop redis"
docker stop redis
echo "docker rm redis"
docker rm redis

echo "docker network rm ${NET_NAME}"
docker network rm ${NET_NAME}


echo "docker stop ${APP_NAME}"
docker stop ${APP_NAME}
echo "docker rm ${APP_NAME}"
docker rm ${APP_NAME}

time minikube start --kubernetes-version=v1.25.13 --memory 16384 --cpus 4  --force

#now set up the demo setup
#istioctl install demo -y
istioctl install --set profile=demo -y




#inject prometheus
#https://istio.io/latest/docs/ops/integrations/prometheus/
minikube kubectl -- apply -f https://raw.githubusercontent.com/istio/istio/release-1.19/samples/addons/prometheus.yaml

#inject grafana;
#https://istio.io/latest/docs/ops/integrations/grafana/
minikube kubectl -- apply -f https://raw.githubusercontent.com/istio/istio/release-1.19/samples/addons/grafana.yaml



#Output images to the LOCAL minicube dealio -- rather than the default.
echo "Point shell output to minikube docker"
echo "eval $(minikube -p minikube docker-env)"
eval $(minikube -p minikube docker-env)

#build docker from the docker file
echo "docker build -t ${IMAGE_NAME} -f ${DOCKER_FILE}"
time docker build -t ${IMAGE_NAME} -f ${DOCKER_FILE} .

#echo "docker run -d --net ${NET_NAME} --name ${APP_NAME} -p 8000:8000 ${IMAGE_NAME} "
#docker run -d --net ${NET_NAME} --name ${APP_NAME} -p 8000:8000 ${IMAGE_NAME} 



cd ./infra
. delete_deployments.sh
sleep 2
my_all_pods=$(minikube kubectl -- get pods --all-namespaces| wc -l)
. apply_deployments.sh
cd ./../
sleep 2
my_all_pods_after_deploy=$(minikube kubectl -- get pods --all-namespaces| wc -l)

echo my_all_pods=$my_all_pods


while [ $my_all_pods_after_deploy -le $my_all_pods ]; do
    my_all_pods_after_deploy=$(minikube kubectl -- get pods --all-namespaces| wc -l)
    #echo my_all_pods=$my_all_pods
    #echo my_all_pods_after_deploy=$my_all_pods_after_deploy
done
echo my_all_pods=$my_all_pods
echo my_all_pods_after_deploy=$my_all_pods_after_deploy

#make sure we have more pods AFTER the scripts than before.

echo "*********************************"
echo "*  ENDING                       *"
echo "* Docker stopping and rebuild   *"
echo "*                               *"
echo "*********************************"



echo "**********************************"
echo "*  STARTING                      *"
echo "* port forwarding                *"
echo "*                                *"
echo "* Make sure all pods are running *"
echo "* Before issuing port forwarding *"
echo "*                                *".
echo "**********************************"

echo $PWD

echo my_all_pods=$(minikube kubectl -- get pods --namespace=w255| wc -l)
echo $my_all_pods
running_pods=$(minikube kubectl -- get pods --namespace=w255 --field-selector=status.phase=Running| wc -l)
echo $running_pods
while [ $running_pods -le $my_all_pods ]; do
    #echo my_all_pods=$(minikube kubectl -- get pods --namespace=w255| wc -l)
    my_all_pods=$(minikube kubectl -- get pods --namespace=w255| wc -l)
    #echo running_pods=$(minikube kubectl -- get pods --namespace=w255 --field-selector=status.phase=Running| wc -l)
    running_pods=$(minikube kubectl -- get pods --namespace=w255 --field-selector=status.phase=Running| wc -l)
    let "running_pods = running_pods+1"
    #echo running_pods=$running_pods

    sleep 1
done

echo my_all_pods=$my_all_pods
echo running_pods=$running_pods

#20230914 don irwin -- disabling below in favor of istio
echo "set up the dashboard"
echo "note this can be done in yaml"
#kubectl create serviceaccount k8sadmin -n kube-system
#kubectl create clusterrolebinding k8sadmin --clusterrole=cluster-admin --serviceaccount=kube-system:k8sadmin
#my_token=kubectl -n kube-system describe secret $(sudo kubectl -n kube-system get secret | (grep k8sadmin || echo "$_") | awk '{print $1}') | grep token: | awk '{print $2}'
#echo $my_token>token.txt

#kubectl proxy --address='0.0.0.0' --disable-filter=true>/dev/null &
#proxy_pid=$!
#minikube dashboard --url >/dev/null&
#echo "Open this creature:"
#echo "http://localhost:8001:/api/v1/namespaces/kubernetes-dashboard/services/http:kubernetes-dashboard:/proxy/"


my_ticks=$(( $(date '+%s%N') / 1000000))

sleep 2

echo "*********************************"
echo "*  BEGIN                        *"
echo "* port forwarding               *"
echo "*                               *"
echo "*********************************"

rm output_*.txt

#consult:
#https://istio.io/latest/docs/setup/platform-setup/minikube/
#
#https://minikube.sigs.k8s.io/docs/handbook/accessing/

#return

echo "port-forward -n w255 Service/frontend 8000:8000 --address='0.0.0.0' > output_$my_ticks.txt & "
kubectl port-forward -n w255 Service/frontend 8000:8000 --address='0.0.0.0' > output_$my_ticks.txt & 


echo "port-forward -n istio-system Service/grafana 3000:3000 --address='0.0.0.0' > output_$my_ticks.txt & "
kubectl port-forward -n istio-system Service/grafana 3000:3000 --address='0.0.0.0' > output_grafana_$my_ticks.txt & 

echo "*********************************"
echo "*                               *"
echo "*  EXTRACTING ip address of     *"
echo "*        load balancer          *"
echo "*                               *"
echo "*********************************"

#kubectl -n kube-system get svc cluster-nginx-ingress-controller -o json | jq 

python_api_address=localhost
export python_api_address=$python_api_address

python setup_values.py



echo "*********************************"
echo "*                               *"
echo "*        WAITING. ....          *"
echo "*        API not ready          *"
echo "*                               *"
echo "*********************************"


finished=false
while ! $finished; do
    health_status=$(curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://${python_api_address}:8000/health")
    if [ $health_status == "200" ]; then
        finished=true
        echo "*********************************"
        echo "*                               *"
        echo "*        API is ready           *"
        echo "http://${python_api_address}:8000/docs"
        echo "*                               *"
        echo "*********************************"
    else
        finished=false
    fi
done
echo""
echo""

echo "*********************************"
echo "*                               *"
echo "*        grafana is ready           *"
echo "http://localhost:3000"
echo "*                               *"
echo "*********************************"



echo "*********************************"
echo "*                               *"
echo "*  RUNNING Load testing         *"
echo "*                               *"
echo "*********************************"

. run_k6.sh

echo "*********************************"
echo "*                               *"
echo "*        WAITING. ....          *"
echo "*        API not ready          *"
echo "*                               *"
echo "*********************************"


finished=false
while ! $finished; do
    health_status=$(curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/health")
    if [ $health_status == "200" ]; then
        finished=true
        echo "*********************************"
        echo "*                               *"
        echo "*        API is ready           *"
        echo "*                               *"
        echo "*********************************"
    else
        finished=false
    fi
done
echo""
echo""


echo "*********************************"
echo "*                               *"
echo "*     Running CURL Calls        *"
echo "*                               *"
echo "*  Note that FASTAPI uses 307   *"
echo "*  internal redirects for its   *"
echo "*  query string parsing unless  *"
echo "*  the request is formed like   *"
echo "*     /hello/?name=Don          *"
echo "*                               *"
echo "*********************************"


IP_ADDRESS="localhost"

CURL_URI="http://localhost:8000/health"

echo "About to call the following URI: ${CURL_URI}"

return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X GET "${CURL_URI}")
curl ${CURL_URI}
echo ""
echo "the return code is : ${return_code}"

CURL_URI="http://localhost:8000/hello/?name=Don"
echo "About to call the following URI: ${CURL_URI}"

curl ${CURL_URI}
echo ""

return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X GET "${CURL_URI}")

echo "the return code is : ${return_code}"

CURL_URI="http://localhost:8000/hello/?nam=Don"
echo "About to call the following URI: ${CURL_URI}"

return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X GET "${CURL_URI}")
curl ${CURL_URI}
echo ""
echo "the return code is : ${return_code}"

CURL_URI="http://localhost:8000/"
echo "About to call the following URI: ${CURL_URI}"

return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X GET "${CURL_URI}")

echo "the return code is : ${return_code}"
curl ${CURL_URI}
echo ""

CURL_URI="http://localhost:8000/docs"
echo "About to call the following URI: ${CURL_URI}"

return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X GET "${CURL_URI}")

echo "the return code is : ${return_code}"
echo ""

CURL_URI="http://localhost:8000/hello?name=Don"
echo "About to call the following URI: ${CURL_URI}"

return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X GET "${CURL_URI}")
curl ${CURL_URI}
echo ""
echo "the return code is : ${return_code}"
echo ""


echo "*********************************"
echo "*                               *"
echo "* Posts to predict -- should    *"
echo "* have 200 return codes         *"
echo "*********************************"

good_return_codes=0
bad_return_codes=0

eval_return () {
  my_code="$1"
  

if [ "$my_code" == "200" ]; then
    let "good_return_codes = good_return_codes+1"
else
    let "bad_return_codes = bad_return_codes+1"
fi

}

echo "*********************************"
echo "* Posts to predict -- should    *"
echo "* have 200 return codes         *"
echo "* We are doing 200 iterations   *"
echo "*********************************"


for i in {1..200}

do
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '[{"MedInc":8.3252,"HouseAge":41.0,"AveRooms":6.984126984126984,"AveBedrms":1.0238095238095237,"Population":322.0,"AveOccup":2.5555555555555554,"Latitude":37.88,"Longitude":-122.23 },{"MedInc":8.3014,"HouseAge":21.0,"AveRooms":6.238137082601054,"AveBedrms":0.9718804920913884,"Population":2401.0,"AveOccup":2.109841827768014,"Latitude":37.86,"Longitude":-122.22 },{"MedInc":5.6431,"HouseAge":52.0,"AveRooms":5.8173515981735155,"AveBedrms":1.0730593607305936,"Population":558.0,"AveOccup":2.547945205479452,"Latitude":37.85,"Longitude":-122.25 }]')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '[{"MedInc":8.3014,"HouseAge":21.0,"AveRooms":6.238137082601054,"AveBedrms":0.9718804920913884,"Population":2401.0,"AveOccup":2.109841827768014,"Latitude":37.86,"Longitude":-122.22 },{"MedInc":3.6591,"HouseAge":52.0,"AveRooms":4.9319066147859925,"AveBedrms":0.9513618677042801,"Population":1094.0,"AveOccup":2.1284046692607004,"Latitude":37.84,"Longitude":-122.25 },{"MedInc":5.6431,"HouseAge":52.0,"AveRooms":5.8173515981735155,"AveBedrms":1.0730593607305936,"Population":558.0,"AveOccup":2.547945205479452,"Latitude":37.85,"Longitude":-122.25 }]')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '[{"MedInc":3.8462,"HouseAge":52.0,"AveRooms":6.281853281853282,"AveBedrms":1.0810810810810811,"Population":565.0,"AveOccup":2.1814671814671813,"Latitude":37.85,"Longitude":-122.25 },{"MedInc":7.2574,"HouseAge":52.0,"AveRooms":8.288135593220339,"AveBedrms":1.073446327683616,"Population":496.0,"AveOccup":2.8022598870056497,"Latitude":37.85,"Longitude":-122.24 },{"MedInc":3.12,"HouseAge":52.0,"AveRooms":4.797527047913447,"AveBedrms":1.061823802163833,"Population":1157.0,"AveOccup":1.7882534775888717,"Latitude":37.84,"Longitude":-122.25 },{"MedInc":3.12,"HouseAge":52.0,"AveRooms":4.797527047913447,"AveBedrms":1.061823802163833,"Population":1157.0,"AveOccup":1.7882534775888717,"Latitude":37.84,"Longitude":-122.25 }]')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '[{"MedInc":3.8462,"HouseAge":52.0,"AveRooms":6.281853281853282,"AveBedrms":1.0810810810810811,"Population":565.0,"AveOccup":2.1814671814671813,"Latitude":37.85,"Longitude":-122.25 },{"MedInc":5.6431,"HouseAge":52.0,"AveRooms":5.8173515981735155,"AveBedrms":1.0730593607305936,"Population":558.0,"AveOccup":2.547945205479452,"Latitude":37.85,"Longitude":-122.25 },{"MedInc":3.12,"HouseAge":52.0,"AveRooms":4.797527047913447,"AveBedrms":1.061823802163833,"Population":1157.0,"AveOccup":1.7882534775888717,"Latitude":37.84,"Longitude":-122.25 },{"MedInc":3.12,"HouseAge":52.0,"AveRooms":4.797527047913447,"AveBedrms":1.061823802163833,"Population":1157.0,"AveOccup":1.7882534775888717,"Latitude":37.84,"Longitude":-122.25 }]')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '[{"MedInc":3.8462,"HouseAge":52.0,"AveRooms":6.281853281853282,"AveBedrms":1.0810810810810811,"Population":565.0,"AveOccup":2.1814671814671813,"Latitude":37.85,"Longitude":-122.25 },{"MedInc":3.8462,"HouseAge":52.0,"AveRooms":6.281853281853282,"AveBedrms":1.0810810810810811,"Population":565.0,"AveOccup":2.1814671814671813,"Latitude":37.85,"Longitude":-122.25 }]')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '[{"MedInc":4.0368,"HouseAge":52.0,"AveRooms":4.761658031088083,"AveBedrms":1.1036269430051813,"Population":413.0,"AveOccup":2.139896373056995,"Latitude":37.85,"Longitude":-122.25 },{"MedInc":3.12,"HouseAge":52.0,"AveRooms":4.797527047913447,"AveBedrms":1.061823802163833,"Population":1157.0,"AveOccup":1.7882534775888717,"Latitude":37.84,"Longitude":-122.25 },{"MedInc":3.12,"HouseAge":52.0,"AveRooms":4.797527047913447,"AveBedrms":1.061823802163833,"Population":1157.0,"AveOccup":1.7882534775888717,"Latitude":37.84,"Longitude":-122.25 }]')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '[{"MedInc":3.6591,"HouseAge":52.0,"AveRooms":4.9319066147859925,"AveBedrms":0.9513618677042801,"Population":1094.0,"AveOccup":2.1284046692607004,"Latitude":37.84,"Longitude":-122.25 },{"MedInc":3.12,"HouseAge":52.0,"AveRooms":4.797527047913447,"AveBedrms":1.061823802163833,"Population":1157.0,"AveOccup":1.7882534775888717,"Latitude":37.84,"Longitude":-122.25 },{"MedInc":3.12,"HouseAge":52.0,"AveRooms":4.797527047913447,"AveBedrms":1.061823802163833,"Population":1157.0,"AveOccup":1.7882534775888717,"Latitude":37.84,"Longitude":-122.25 }]')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '[{"MedInc":3.12,"HouseAge":52.0,"AveRooms":4.797527047913447,"AveBedrms":1.061823802163833,"Population":1157.0,"AveOccup":1.7882534775888717,"Latitude":37.84,"Longitude":-122.25 },{"MedInc":3.12,"HouseAge":52.0,"AveRooms":4.797527047913447,"AveBedrms":1.061823802163833,"Population":1157.0,"AveOccup":1.7882534775888717,"Latitude":37.84,"Longitude":-122.25 }]')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '[{"MedInc":2.0804,"HouseAge":42.0,"AveRooms":4.294117647058823,"AveBedrms":1.1176470588235294,"Population":1206.0,"AveOccup":2.026890756302521,"Latitude":37.84,"Longitude":-122.26 },{"MedInc":3.12,"HouseAge":52.0,"AveRooms":4.797527047913447,"AveBedrms":1.061823802163833,"Population":1157.0,"AveOccup":1.7882534775888717,"Latitude":37.84,"Longitude":-122.25 },{"MedInc":3.12,"HouseAge":52.0,"AveRooms":4.797527047913447,"AveBedrms":1.061823802163833,"Population":1157.0,"AveOccup":1.7882534775888717,"Latitude":37.84,"Longitude":-122.25 }]')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '[{"MedInc":3.6912,"HouseAge":52.0,"AveRooms":4.970588235294118,"AveBedrms":0.9901960784313726,"Population":1551.0,"AveOccup":2.172268907563025,"Latitude":37.84,"Longitude":-122.25 },{"MedInc":3.12,"HouseAge":52.0,"AveRooms":4.797527047913447,"AveBedrms":1.061823802163833,"Population":1157.0,"AveOccup":1.7882534775888717,"Latitude":37.84,"Longitude":-122.25 },{"MedInc":3.12,"HouseAge":52.0,"AveRooms":4.797527047913447,"AveBedrms":1.061823802163833,"Population":1157.0,"AveOccup":1.7882534775888717,"Latitude":37.84,"Longitude":-122.25 }]')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '[{"MedInc":3.12,"HouseAge":52.0,"AveRooms":4.797527047913447,"AveBedrms":1.061823802163833,"Population":1157.0,"AveOccup":1.7882534775888717,"Latitude":37.84,"Longitude":-122.25 },{"MedInc":3.12,"HouseAge":52.0,"AveRooms":4.797527047913447,"AveBedrms":1.061823802163833,"Population":1157.0,"AveOccup":1.7882534775888717,"Latitude":37.84,"Longitude":-122.25 },{"MedInc":3.2031,"HouseAge":52.0,"AveRooms":5.477611940298507,"AveBedrms":1.0796019900497513,"Population":910.0,"AveOccup":2.263681592039801,"Latitude":37.85,"Longitude":-122.26 }]')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '[{"MedInc":3.12,"HouseAge":52.0,"AveRooms":4.797527047913447,"AveBedrms":1.061823802163833,"Population":1157.0,"AveOccup":1.7882534775888717,"Latitude":37.84,"Longitude":-122.25 },{"MedInc":3.12,"HouseAge":52.0,"AveRooms":4.797527047913447,"AveBedrms":1.061823802163833,"Population":1157.0,"AveOccup":1.7882534775888717,"Latitude":37.84,"Longitude":-122.25 },{"MedInc":3.2705,"HouseAge":52.0,"AveRooms":4.772479564032698,"AveBedrms":1.0245231607629428,"Population":1504.0,"AveOccup":2.0490463215258856,"Latitude":37.85,"Longitude":-122.26 }]')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '[{"MedInc":3.075,"HouseAge":52.0,"AveRooms":5.322649572649572,"AveBedrms":1.0128205128205128,"Population":1098.0,"AveOccup":2.3461538461538463,"Latitude":37.85,"Longitude":-122.26 },{"MedInc":3.075,"HouseAge":52.0,"AveRooms":5.322649572649572,"AveBedrms":1.0128205128205128,"Population":1098.0,"AveOccup":2.3461538461538463,"Latitude":37.85,"Longitude":-122.26 }]')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '[{"MedInc":2.6736,"HouseAge":52.0,"AveRooms":4.0,"AveBedrms":1.0977011494252873,"Population":345.0,"AveOccup":1.9827586206896552,"Latitude":37.84,"Longitude":-122.26 },{"MedInc":2.6736,"HouseAge":52.0,"AveRooms":4.0,"AveBedrms":1.0977011494252873,"Population":345.0,"AveOccup":1.9827586206896552,"Latitude":37.84,"Longitude":-122.26 }]')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '[{"MedInc":1.9167,"HouseAge":52.0,"AveRooms":4.262903225806451,"AveBedrms":1.0096774193548388,"Population":1212.0,"AveOccup":1.9548387096774194,"Latitude":37.85,"Longitude":-122.26 },{"MedInc":1.9167,"HouseAge":52.0,"AveRooms":4.262903225806451,"AveBedrms":1.0096774193548388,"Population":1212.0,"AveOccup":1.9548387096774194,"Latitude":37.85,"Longitude":-122.26 }]')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '[{"MedInc":2.125,"HouseAge":50.0,"AveRooms":4.242424242424242,"AveBedrms":1.071969696969697,"Population":697.0,"AveOccup":2.640151515151515,"Latitude":37.85,"Longitude":-122.26 },{"MedInc":2.125,"HouseAge":50.0,"AveRooms":4.242424242424242,"AveBedrms":1.071969696969697,"Population":697.0,"AveOccup":2.640151515151515,"Latitude":37.85,"Longitude":-122.26 }]')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '[{"MedInc":2.775,"HouseAge":52.0,"AveRooms":5.9395770392749245,"AveBedrms":1.0483383685800605,"Population":793.0,"AveOccup":2.395770392749245,"Latitude":37.85,"Longitude":-122.27 },{"MedInc":2.775,"HouseAge":52.0,"AveRooms":5.9395770392749245,"AveBedrms":1.0483383685800605,"Population":793.0,"AveOccup":2.395770392749245,"Latitude":37.85,"Longitude":-122.27 }]')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '[{"MedInc":1.3578,"HouseAge":40.0,"AveRooms":4.524096385542169,"AveBedrms":1.108433734939759,"Population":409.0,"AveOccup":2.463855421686747,"Latitude":37.85,"Longitude":-122.27 },{"MedInc":2.1202,"HouseAge":52.0,"AveRooms":4.052805280528053,"AveBedrms":0.966996699669967,"Population":648.0,"AveOccup":2.1386138613861387,"Latitude":37.85,"Longitude":-122.27 }]')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '[{"MedInc":1.9911,"HouseAge":50.0,"AveRooms":5.343675417661098,"AveBedrms":1.0859188544152745,"Population":990.0,"AveOccup":2.3627684964200477,"Latitude":37.84,"Longitude":-122.26 },{"MedInc":1.9911,"HouseAge":50.0,"AveRooms":5.343675417661098,"AveBedrms":1.0859188544152745,"Population":990.0,"AveOccup":2.3627684964200477,"Latitude":37.84,"Longitude":-122.26 }]')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '[{"MedInc":2.6033,"HouseAge":52.0,"AveRooms":5.465454545454546,"AveBedrms":1.0836363636363637,"Population":690.0,"AveOccup":2.5090909090909093,"Latitude":37.84,"Longitude":-122.27 },{"MedInc":2.6033,"HouseAge":52.0,"AveRooms":5.465454545454546,"AveBedrms":1.0836363636363637,"Population":690.0,"AveOccup":2.5090909090909093,"Latitude":37.84,"Longitude":-122.27 }]')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '[{"MedInc":1.3578,"HouseAge":40.0,"AveRooms":4.524096385542169,"AveBedrms":1.108433734939759,"Population":409.0,"AveOccup":2.463855421686747,"Latitude":37.85,"Longitude":-122.27 },{"MedInc":1.3578,"HouseAge":40.0,"AveRooms":4.524096385542169,"AveBedrms":1.108433734939759,"Population":409.0,"AveOccup":2.463855421686747,"Latitude":37.85,"Longitude":-122.27 }]')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '[{"MedInc":1.7135,"HouseAge":42.0,"AveRooms":4.478142076502732,"AveBedrms":1.0027322404371584,"Population":929.0,"AveOccup":2.5382513661202184,"Latitude":37.85,"Longitude":-122.27 },{"MedInc":1.7135,"HouseAge":42.0,"AveRooms":4.478142076502732,"AveBedrms":1.0027322404371584,"Population":929.0,"AveOccup":2.5382513661202184,"Latitude":37.85,"Longitude":-122.27 }]')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '[{"MedInc":1.7135,"HouseAge":42.0,"AveRooms":4.478142076502732,"AveBedrms":1.0027322404371584,"Population":929.0,"AveOccup":2.5382513661202184,"Latitude":37.85,"Longitude":-122.27 },{"MedInc":1.725,"HouseAge":52.0,"AveRooms":5.096234309623431,"AveBedrms":1.1317991631799162,"Population":1015.0,"AveOccup":2.1234309623430963,"Latitude":37.84,"Longitude":-122.27 }]')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '[{"MedInc":2.1806,"HouseAge":52.0,"AveRooms":5.193846153846154,"AveBedrms":1.0369230769230768,"Population":853.0,"AveOccup":2.624615384615385,"Latitude":37.84,"Longitude":-122.27 },{"MedInc":2.1806,"HouseAge":52.0,"AveRooms":5.193846153846154,"AveBedrms":1.0369230769230768,"Population":853.0,"AveOccup":2.624615384615385,"Latitude":37.84,"Longitude":-122.27 }]')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '[{"MedInc":2.6,"HouseAge":52.0,"AveRooms":5.270142180094787,"AveBedrms":1.0355450236966826,"Population":1006.0,"AveOccup":2.3838862559241707,"Latitude":37.84,"Longitude":-122.27 },{"MedInc":2.6,"HouseAge":52.0,"AveRooms":5.270142180094787,"AveBedrms":1.0355450236966826,"Population":1006.0,"AveOccup":2.3838862559241707,"Latitude":37.84,"Longitude":-122.27 }]')
eval_return "${return_code}"

done



echo "*********************************"
echo "* END OF GOOD 200 ZONE          *"
echo "* Posts to predict -- should    *"
echo "* have 200 return codes         *"
echo "*********************************"

echo "good_return_codes=${good_return_codes}"
echo "bad_return_codes=${bad_return_codes}"

echo "*********************************"
echo "* BEGINNING OF BAD ZONE         *"
echo "* Posts to predict -- should    *"
echo "* NOT have 200 return codes     *"
echo "*********************************"

return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '{"MedInc":8.3252,"HouseAge":41.0,"AveRooms":6.984126984126984,"AveBedrms":1.0238095238095237,"Population":322.0,"AveOccup":2.5555555555555554,"Latitude":37.88,"Longitude":-122.23, "fido" : "dido" }')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '{"MedInc":8.3014,"HouseAge":21.0,"AveRooms":6.238137082601054,"AveBedrms":0.9718804920913884,"Population":2401.0,"AveOccup":2.109841827768014,"Latitude":37.86,"Longitude":-122.22 , "fido" : "dido" }')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '{"MedInc":7.2574,"HouseAge":52.0,"AveRooms":8.288135593220339,"AveBedrms":1.073446327683616,"Population":496.0,"AveOccup":2.8022598870056497,"Latitude":"bozo","Longitude":-122.24 }')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '{"MedInc":5.6431,"HouseAge":52.0,"AveRooms":5.8173515981735155,"AveBedrms":1.0730593607305936,"Population":558.0,"AveOccup":2.547945205479452,"Latitude":"jumk","Longitude":-122.25 }')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '{"MedInc":3.8462,"HouseAge":52.0,"AveRooms":6.281853281853282,"AveBedrms":1.0810810810810811,"Population":565.0,"AveOccup":2.1814671814671813,"Latitude":37.85,"Longitude":"fido" }')
eval_return "${return_code}"
return_code=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H 'Content-Type: application/json' localhost:8000/predict -d '{"MedInc":4.0368,"HouseAge":52.0,"AveRooms":4.761658031088083,"AveBedrms":1.1036269430051813,"Population":413.0,"AveOccup":2.139896373056995,"Latitude":37.85,"Longitude":-122.25 , "fido" : "dido" }')

echo "*********************************"
echo "* END OF BAD ZONE               *"
echo "* Posts to predict -- should    *"
echo "* NOT have 200 return codes     *"
echo "*********************************"

echo "good_return_codes=${good_return_codes}"
echo "bad_return_codes=${bad_return_codes}"


echo "*********************************"
echo "*                               *"
echo "*        End of bash handling   *"
echo "*                               *"
echo "*********************************"


echo "*********************************"
echo "*   End of Event Pitching      *"
echo "*********************************"

echo "*********************************"
echo "*   Expected                    *"
echo "*********************************"

echo "good_return_codes=5000"
echo "bad_return_codes=5"

echo "*********************************"
echo "*   Actual                      *"
echo "*********************************"
echo "good_return_codes=${good_return_codes}"
echo "bad_return_codes=${bad_return_codes}"

    if [ $good_return_codes == "5000" ]; then
        if [ $bad_return_codes == "5" ]; then

            echo "*********************************"
            echo "*   RETURN CODE COUNT           *"
            echo "*                               *"            
            echo "*   MATCH: Good                 *"
            echo "*                               *"
            echo "*********************************"

        fi

    else

            echo "*********************************"
            echo "*   RETURN CODE COUNT           *"
            echo "*                               *"            
            echo "*   MATCH: Bad                  *"
            echo "*                               *"
            echo "*********************************"
    fi


export W255_UP=1

. run_k6.sh

#this shell expots a do_exit value
. do_exit.sh
if [[ "$do_exit" -eq 1 ]]
then
cd ./infra
. delete_deployments.sh
cd ./../
minikube stop
export W255_UP=0
return
fi

