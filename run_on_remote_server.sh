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
echo "* Architect: Don Irwin           "
echo "* Primary difference between     "
echo "* This and run.sh is  "
echo "* The kubectl files are wrapped for running in non-interactive shell"
echo "* I.E.:"
echo "*\$(minikube kubectl -- get pods --all-namespaces| wc -l)"
echo "* RATHER THAN: "
echo "*\$(kubectl get pods --all-namespaces| wc -l)"
echo "* "
echo "**********************************"


echo "**********************************"
echo "* Loosely based on the project   *"
echo "* Below                          *"
echo "**********************************"


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

# echo "port-forward -n w255 Service/frontend 8000:8000 --address='0.0.0.0' > output_$my_ticks.txt & "
# kubectl port-forward -n w255 Service/frontend 8000:8000 --address='0.0.0.0' > output_$my_ticks.txt & 


# while ${prompt_for_minikube}; do
#         echo "*********************************"
#         echo "                               "
#         echo " We are about to run the command "
#         echo "                               "  
#         echo "Starting the port forwarding -- this will end the process"
#         echo "nohup minikube tunnel &        "      
#         echo "                               "
#         echo "Special settings need to be in place"
#         echo "                               "
#         echo "If they are not in place       "
#         echo "This needs to be run in a new  "
#         echo "Window under sudo             "
#         echo "See the following URLs:        "
#         echo "https://minikube.sigs.k8s.io/docs/handbook/accessing/"
#         echo "https://superuser.com/questions/1328452/sudoers-nopasswd-for-single-executable-but-allowing-others"
#         echo "                               "
#         echo "                               "
#         echo " DO YOU HAVE NOPASSWD SET UP   "
#         echo " FOR commands \"ip\" and \"route\"          "
#         echo "                               "
#         echo " If run this in a separate terminal:"
#         echo "\"minikube tunnel "        "      
#         echo "  Then Answer \"n"         "

#         echo "                               "

#         echo "*********************************"
#         while true; do
#             read -p "Do you have permissions set up? [y/n]:" yn
#             case $yn in
#                 [Yy]* ) do_minikube_tunnel=1;break;;
#                 [Nn]* ) do_minikube_tunnel=0;break;;
#                 * ) echo "Please answer \"y\" or \"n\".";;
#             esac
#         done        
# break
 
# done

do_minikube_tunnel=1
if [[ "$do_minikube_tunnel" -eq 1 ]]
then
echo "*********************************"
echo "* running:                      *"
echo "*nohup minikube tunnel &        *"
echo "*                               *"
echo "*********************************"
echo "Starting the port forwarding"
rm nohup.out
sudo nohup minikube tunnel &

port_forwarding_pid=$!

fi



echo "* port_forwarding_pid=$port_forwarding_pid*"


echo "port-forward -n istio-system Service/grafana 3000:3000 --address='0.0.0.0' > output_$my_ticks.txt & "
kubectl port-forward -n istio-system Service/grafana 3000:3000 --address='0.0.0.0' > output_grafana_$my_ticks.txt & 

sleep 10

echo "*********************************"
echo "*  ENDING                       *"
echo "* port forwarding               *"
echo "* port_forwarding_pid=$port_forwarding_pid*"
echo "*********************************"
cat nohup.out
sleep 1

echo "*********************************"
echo "*                               *"
echo "*  EXTRACTING ip address of     *"
echo "*        load balancer          *"
echo "*                               *"
echo "*********************************"

#kubectl -n kube-system get svc cluster-nginx-ingress-controller -o json | jq 

python_api_address=$(minikube kubectl -- -n w255 get svc frontend -o json | jq -r ".status.loadBalancer.ingress[0].ip")
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

#this shell expots a do_exit value
. do_exit.sh
if [[ "$do_exit" -eq 1 ]]
then
cd ./infra
. delete_deployments.sh
cd ./../
sudo kill $port_forwarding_pid
minikube stop
export W255_UP=0
return
fi



