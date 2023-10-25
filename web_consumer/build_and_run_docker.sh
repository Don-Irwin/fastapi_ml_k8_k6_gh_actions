#!/bin/bash
#get_environment_variables
source ./env.sh


#docker rmi $(docker images --filter "dangling=true" -q --no-trunc)

echo "docker stop ${APP_NAME_WC}"
docker stop ${APP_NAME_WC}
echo "docker rm ${APP_NAME_WC}"
docker rm ${APP_NAME_WC}

#build docker from the docker file
echo "docker build -t ${IMAGE_NAME_WC} -f ${DOCKER_FILE_WC}" 
docker build -t ${IMAGE_NAME_WC} -f ${DOCKER_FILE_WC} .
echo "docker run --name ${APP_NAME_WC} -p  8888:8888 -p 5000:5000  ${IMAGE_NAME_WC} "
docker run --name ${APP_NAME_WC} -p  8888:8888 -p 5000:5000  ${IMAGE_NAME_WC} >/dev/null & 


finished=false
while ! $finished; do
    health_status=$(curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://127.0.0.1:5000")
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
echo "* http://127.0.0.1:5000           *"
echo "*                                 *"
echo "***********************************"
# finished=false
# while ! $finished; do
#     health_status=$(curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://127.0.0.1:8888/tree")
#     if [ $health_status == "200" ]; then
#         finished=true
#         echo "*********************************"
#         echo "*                               *"
#         echo "*      Jyputer is ready         *"
#         echo "*                               *"
#         echo "*********************************"
#     else
#         finished=false
#     fi
# done

# echo "***********************************"
# echo "*                                 *"
# echo "* Access Jupyter at the following *"
# echo "* Address                         *"
# echo "* http://127.0.0.1:8888/tree?     *"
# echo "*                                 *"
# echo "***********************************"
