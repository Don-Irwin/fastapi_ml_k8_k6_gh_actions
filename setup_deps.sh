#!/bin/bash

    export PATH=$(cat /etc/environment)

    all_deps=0
    username="ubuntu"

    if id "$username" &>/dev/null; then
        echo "User $username already exists."
    else
        echo "User $username does not exist, creating user..."
        sudo adduser --disabled-password --gecos "" "$username"
        echo "User $username has been created with no password."
    fi

    apt update

    #remove prompting on auto builds
    apt-get remove needrestart -y

    apt install curl -y

    docker ps >/dev/null
    let "all_deps=$all_deps+$?"
    docker ps >/dev/null
    if [ $? -eq 0 ]; then
        echo "docker installed"
    else
        apt install docker -y
    fi

    docker-compose --help >/dev/null
    let "all_deps=$all_deps+$?"
    docker-compose --help >/dev/null
    if [ $? -eq 0 ]; then

        echo "docker-compose installed"
    else
        apt install docker-compose -y
    fi

    git --help >/dev/null
    let "all_deps=$all_deps+$?"
    git --help >/dev/null
    if [ $? -eq 0 ]; then

        echo "git installed"
    else
        apt install git -y
    fi

    #install core stuff
     apt install python-is-python3 -y && apt install nano -y

    poetry --version >/dev/null
    let "all_deps=$all_deps+$?"
    poetry --version >/dev/null    
    if [ $? -eq 0 ]; then

        echo "poetry installed"
    else
        #get poetry
        curl -sSL https://install.python-poetry.org | POETRY_HOME=/ python -
    fi

    minikube --help >/dev/null
    let "all_deps=$all_deps+$?"
    minikube --help >/dev/null
    if [ $? -eq 0 ]; then

        echo "minikube installed"
    else
        #get minikube
        curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
        install minikube-linux-amd64 /usr/local/bin/minikube
    fi

    k6 --help >/dev/null
    let "all_deps=$all_deps+$?"
    k6 --help >/dev/null
    if [ $? -eq 0 ]; then

        echo "k6 installed"
    else
        #get k6
        snap install k6
        export PATH="$PATH:/snap/bin/"
        echo $PATH>/etc/environment
        cat /etc/environment

    fi


    istioctl --help >/dev/null
    let "all_deps=$all_deps+$?"
    istioctl --help >/dev/null
    if [ $? -eq 0 ]; then

        echo "istioctl installed"
    else
        #istio
        curl -L https://istio.io/downloadIstio | ISTIO_VERSION=1.19.0 TARGET_ARCH=x86_64 sh -
        chmod 777 -R  istio-1.19.0
        export PATH="$PATH:$(pwd)/istio-1.19.0/bin/"
        echo $PATH>/etc/environment
        cat /etc/environment

    fi


    kubectl --help >/dev/null
    let "all_deps=$all_deps+$?"
    kubectl --help >/dev/null
    if [ $? -eq 0 ]; then

        echo "kubectl installed"
    else
        curl -LO https://dl.k8s.io/release/v1.28.1/bin/linux/amd64/kubectl
        install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
    fi


    nginx -v >/dev/null
    let "all_deps=$all_deps+$?"
    nginx -v >/dev/null
    if [ $? -eq 0 ]; then
        echo "nginx installed"
    else
        #make this last
        apt install nginx -y
    fi


    #allow other processes to write to directory
    chmod -R 777 /var/www/html/

    usermod -aG docker ubuntu
    usermod -aG docker $(logname)
    newgrp docker

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
        echo "******************************"
    fi
