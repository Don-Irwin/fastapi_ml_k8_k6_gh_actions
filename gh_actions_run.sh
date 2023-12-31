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
    echo 
    mkdir -p ~/.local/bin
    mv ./istio-1.19.0 ~/.local/bin/istio-1.19.0
    export PATH=$PATH:~/.local/bin/istio-1.19.0/bin
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
echo "*   poetry run pytest -vv -s --ignore=./web_consumer   *"
echo "*                               *"
echo "*********************************"

poetry run pytest -vv -s --ignore=./web_consumer
if [ $? -ne 0 ]; then

    echo "*********************************"
    echo "*  FINISHED                     *"
    echo "* Running app locally poetry    *"
    echo "*   poetry run pytest -vv -s --ignore=./web_consumer   *"
    echo "*  FAILURE                      *"
    echo "*********************************"
    return

fi

echo "*********************************"
echo "*  FINISHED                     *"
echo "* Running app locally poetry    *"
echo "*   poetry run pytest -vv -s  --ignore=./web_consumer  *"
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

#kill the web_consumer docker image
cd ./web_consumer
source ./rm_docker_images.sh
cd ./../


time minikube start --kubernetes-version=v1.25.13 --memory 10240 --cpus 4  --force
#16 gb
#time minikube start --kubernetes-version=v1.25.13 --memory 16384 --cpus 4  --force

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

#Now build up the web consumer into minikube
this_dir=$(pwd)
cd ./web_consumer
time . build_docker.sh
cd $this_dir


echo "*********************************"
echo "*  ENDING                       *"
echo "* Completed the docker builds   *"
echo "*                               *"
echo "*********************************"

