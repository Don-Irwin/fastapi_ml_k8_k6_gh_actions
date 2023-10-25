#!/bin/bash

#this shell expots a do_exit value
#prompt for $do_exit
. do_exit.sh

#set it manually
#do_exit=0



#check if the user wants to exit
if [[ "$do_exit" -eq 1 ]]
then
cd ./infra
. delete_deployments.sh
cd ./../
#sudo kill $port_forwarding_pid
minikube stop
export W255_UP=0
return
fi


