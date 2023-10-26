# Serving ML Models With FASTAPI, Redis, Kubernetes, Itsio, Grafana, and Consuming API within Flask

![Visual Overview](images/tech_stack.png)

This system is designed to demonstrate how to serve ML Models utilizing FASTAPI within docker containers built into a Kubernetes environment.

Istio, Prometheus, and are used Grafana within the Kubernetes clster in order to provide visibility to the inner workings of the cluster and its health.

A Flask Web Application is made available in order to demostrate to human users how to consume this API.

The system includes automated Load Testing of the Kubernetes Pod utilizing K6.

Github actions are used to test the health of the solution upon check-in, simulating a production CI/CD health check system.

The solution is a infrastructure as code pure-play.

## Visual Overview

### The Cluster Setup

![Visual Overview](images/serve_ml.drawio.png)

### What Fast API Looks Like

![Visual Overview](images/fast_api.png)

### What the Flask Web Application Looks Like

![Visual Overview](images/flask.png)

## System Requirements

This has been tested on a Linux Ubuntu Server running on a INTEL/AMD64/X86 instruction set microprocessor.

It has not been tested on Mac or OSX.  Some of the exotic port forwarding features of this system require considerable finessing to get them to work on MacOS.

I have not had the time to create a distro for that environment.

If you wish to run this, but do not have a suitable computer, it has been tested on AWS EC2 Instances, Azure virtual machines, and GCP virtual machines.

## Pre-Requisites -- Ubuntu Script Supplied

This project requires many pre-requisites, git, python, docker, docker-compose, minikube, istio, kubectl, bash and others.

Press Ctrl + Click on this link; [setup_deps.sh](https://github.com/Don-Irwin/fastapi_ml_k8_k6_gh_actions/blob/main/setup_deps.sh), to open the `setup_deps.sh` shell file, which will up all of the dependencies on a "blank" server or Virtual Machine with the latest version of Ubuntu.

