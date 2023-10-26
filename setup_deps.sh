#!/bin/bash

    username="ubuntu"

    if id "$username" &>/dev/null; then
        echo "User $username already exists."
    else
        echo "User $username does not exist, creating user..."
        sudo useradd --disabled-password "$username"
        echo "User $username has been created with no password."
    fi

    apt update

    #remove prompting on auto builds
    apt-get remove needrestart -y

    #install core stuff
    apt install docker -y && apt install docker-compose -y && apt install git -y && apt install python-is-python3 -y && apt install nano -y

    #get poetry
    curl -sSL https://install.python-poetry.org | POETRY_HOME=/ python -

    #get minikube
    curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
    install minikube-linux-amd64 /usr/local/bin/minikube

    #get k6
    snap install k6

    #istio
    #istio
    curl -L https://istio.io/downloadIstio | ISTIO_VERSION=1.19.0 TARGET_ARCH=x86_64 sh -
    chmod 777 -R  istio-1.19.0
    rm -rf /usr/local/bin/istio-1.19.0
    mv ./istio-1.19.0 /usr/local/bin/istio-1.19.0
    echo "PATH=$PATH:/usr/local/bin/istio-1.19.0/bin/">>/home/ubuntu/.bashrc
    export PATH="$PATH:/usr/local/bin/istio-1.19.0/bin/"
    echo "PATH=\"$PATH\"">/etc/environment

    curl -LO https://dl.k8s.io/release/v1.28.1/bin/linux/amd64/kubectl
    install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl


    #make this last
    apt install nginx -y

    #allow other processes to write to directory
    chmod -R 777 /var/www/html/

    usermod -aG docker ubuntu
    newgrp docker
