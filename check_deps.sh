#!/bin/bash

    export PATH=$(cat /etc/environment)

echo "Before newgrp"

/usr/bin/newgrp docker <<EONG
echo "hello from within newgrp"

EONG

    echo "After newgrp"

    all_deps=0

    sleep 1
    docker ps >/dev/null
    let "all_deps=$all_deps+$?"
    docker ps >/dev/null
    if [ $? -eq 0 ]; then
        echo "docker installed"
    else
        echo "docker NOT installed"
    fi


    docker-compose --help >/dev/null
    let "all_deps=$all_deps+$?"
    docker-compose --help >/dev/null
    if [ $? -eq 0 ]; then
        echo "docker-compose installed"
    else
        echo "docker-compose NOT installed"
    fi

    git --help >/dev/null
    let "all_deps=$all_deps+$?"
    git --help >/dev/null
    if [ $? -eq 0 ]; then

        echo "git installed"
    else
        echo "git NOT installed"
    fi

    #install core stuff
     apt install python-is-python3 -y && apt install nano -y

    poetry --version >/dev/null
    let "all_deps=$all_deps+$?"
    poetry --version >/dev/null    
    if [ $? -eq 0 ]; then

        echo "poetry installed"
    else
        echo "poetry NOT installed"
    fi

    minikube --help >/dev/null
    let "all_deps=$all_deps+$?"
    minikube --help >/dev/null
    if [ $? -eq 0 ]; then

        echo "minikube installed"
    else
        echo "minikube NOT installed"
    fi

    k6 --help >/dev/null
    let "all_deps=$all_deps+$?"
    k6 --help >/dev/null
    if [ $? -eq 0 ]; then
        echo "k6 installed"
    else
        echo "k6 NOT installed"
    fi


    istioctl --help >/dev/null
    let "all_deps=$all_deps+$?"
    istioctl --help >/dev/null
    if [ $? -eq 0 ]; then
        echo "istioctl installed"
    else
        echo "istioctl NOT installed"
    fi


    kubectl --help >/dev/null
    let "all_deps=$all_deps+$?"
    kubectl --help >/dev/null
    if [ $? -eq 0 ]; then
        echo "kubectl installed"
    else
        echo "kubectl NOT installed"
    fi


    nginx -v >/dev/null
    let "all_deps=$all_deps+$?"
    nginx -v >/dev/null
    if [ $? -eq 0 ]; then
        echo "nginx installed"
    else
        echo "nginx NOT installed"
    fi


    echo PATH=$PATH
    echo all_deps=$all_deps
    if [ $all_deps -ne 0 ]; then
        echo "******************************"
        echo " not all dependencies have been installed"
        echo " re-run: "
        echo "sudo bash ./setup_deps.sh"
        echo " to see if this corrects the issue."
        echo "******************************"
    else
        echo "******************************"
        echo " All Dependencies have been installed."
        echo " In some cases, though, it may be necessary to reboot."        
        echo " This is especially true if docker was not setup prior to this installation."        
        echo "******************************"
    fi
