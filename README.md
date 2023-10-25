#### U.C. Berkeley MIDS W255
#### Summer 2022
#### Instructor: James York Winegar 
#### Student: Don Irwin
#### Lab 3 Submission


### System Pre-requisites: We Assume OSX or Linux System:

1.  Docker.  
2.  Python 3.10.
3.  Poetry.
4.  PIP3.
5.  Minikube.


### Run Steps:

1.   Clone the Repository: -- Get the repository locally
   - Command:  
      git clone https://github.com/UCB-W255/summer22-Tuneman7/
2.   Navigate to directory: -- Move into the lab directory.
   -  Command:    
      cd \*man7/lab_3/lab3
3.   Run the \"run.sh\" bash file:
   - Command:
      . run.sh
4.   Evaluate Output:
   - This should look something like this:

```{text}
**********************************
* U.C. Berkeley MIDS W255        *
* Summer 2022                    *
* Instructor: James York Winegar *
* Student: Don Irwin             *
* Lab 3 Submission               *
**********************************
*********************************
*                               *
* Recycle kubernetes            *
*                               *
*********************************
✋  Stopping node "minikube"  ...
🛑  1 node stopped.
😄  minikube v1.26.0 on Ubuntu 22.04
    ▪ MINIKUBE_ACTIVE_DOCKERD=minikube
🆕  Kubernetes 1.24.1 is now available. If you would like to upgrade, specify: --kubernetes-version=v1.24.1
✨  Using the docker driver based on existing profile
👍  Starting control plane node minikube in cluster minikube
🚜  Pulling base image ...
📌  Noticed you have an activated docker-env on docker driver in this terminal:
🔄  Restarting existing docker container for "minikube" ...
🐳  Preparing Kubernetes v1.22.6 on Docker 20.10.17 ...
🔎  Verifying Kubernetes components...
    ▪ Using image kubernetesui/dashboard:v2.6.0
    ▪ Using image kubernetesui/metrics-scraper:v1.0.8
    ▪ Using image gcr.io/k8s-minikube/storage-provisioner:v5
🌟  Enabled addons: storage-provisioner, default-storageclass, dashboard

    ▪ Want kubectl v1.22.6? Try 'minikube kubectl -- get pods -A'
🏄  Done! kubectl is now configured to use "minikube" cluster and "default" namespace by default
*********************************
*                               *
* finished recycle k8           *
*                               *
*********************************
*********************************
*                               *
* recycle redis and create      *
*   docker network              *
*   redis outside of minicube   *
*   is needed for testing       *
*                               *
*********************************
docker stop redis
redis
docker rm redis
redis
docker network rm w255
w255
docker network create rm w255 
49d397d7ff69da1d6f5257802e23df13eafc14042b2f926160669180095a8604
docker run -d --name redis -p 6379:6379 redis --net w255
2b04417243df2f77198cc417e3494a35ad015163b4d636d2970acbdcfed65dc8
*********************************
*                               *
* Installing Dependencies       *
*   poetry install              *
*                               *
*********************************
Installing dependencies from lock file

No dependencies to install or update

Installing the current project: src (0.1.0)
*********************************
*                               *
* Training the model and writing*
*   *.pkl file                  *
*                               *
*********************************
./src/model_pipeline.pkl exists.
*********************************
*                               *
* Copying pkl file to the src   *
*   *.pkl file                  *
*                               *
*********************************
*********************************
*                               *
* Running app locally poetry    *
*   poetry run pytest -vv -s    *
*                               *
*********************************
============================= test session starts ==============================
platform linux -- Python 3.10.4, pytest-7.1.2, pluggy-1.0.0 -- /home/don/.cache/pypoetry/virtualenvs/src-Sv4jfaDs-py3.10/bin/python
cachedir: .pytest_cache
rootdir: /data/school/MIDS/w255/ucb_githubs/summer22-Tuneman7/lab_3/lab3
plugins: anyio-3.6.1
collecting ... collected 9 items

tests/test_src.py::test_version PASSED
tests/test_src.py::test_read_main PASSED
tests/test_src.py::test_read_hello PASSED
tests/test_src.py::test_read_hello_no_param PASSED
tests/test_src.py::test_read_hello_wrong_param PASSED
tests/test_src.py::test_read_docs PASSED
tests/test_src.py::test_check_health_health PASSED
tests/test_src.py::test_predict_function predicted_value= [3.06795941 3.06795941]
PASSED
tests/test_src.py::test_getcacheratio_function ***got from cache****
predicted_value= [3.06795941 3.06795941]
predict_calls 4
The Hit Ratio: 4 1 0.25
PASSED

============================== 9 passed in 0.49s ===============================
*********************************
*  FINISHED                     *
* Running app locally poetry    *
*   poetry run pytest -vv -s    *
*                               *
*********************************
*********************************
*  STARTING                     *
* Docker stopping and rebuild   *
*                               *
*********************************
docker stop w255_lab3_don_irwin
docker rm w255_lab3_don_irwin
Point shell output to minikube docker
eval export DOCKER_TLS_VERIFY="1"
export DOCKER_HOST="tcp://192.168.49.2:2376"
export DOCKER_CERT_PATH="/home/don/.minikube/certs"
export MINIKUBE_ACTIVE_DOCKERD="minikube"

# To point your shell to minikube's docker-daemon, run:
# eval $(minikube -p minikube docker-env)
docker build -t w255_lab3_don_irwin -f Dockerfile.255lab3
Sending build context to Docker daemon  2.378MB

Step 1/19 : ARG APP_DIR=/app
Step 2/19 : FROM python:3.10-slim-buster AS build
 ---> d82a8f78877e
Step 3/19 : ARG APP_DIR
 ---> Using cache
 ---> d58c47c39f2f
Step 4/19 : RUN apt-get update && apt-get install -y   curl   build-essential   libffi-dev   sudo    && rm -rf /var/lib/apt/lists/*
 ---> Using cache
 ---> 6fab34c1697f
Step 5/19 : ENV POETRY_VERSION=1.1.12
 ---> Using cache
 ---> 23f85ab43f00
Step 6/19 : RUN curl -sSL https://install.python-poetry.org | python -
 ---> Using cache
 ---> 4f7b102d4fe2
Step 7/19 : ENV PATH /root/.local/bin:$PATH
 ---> Using cache
 ---> 8a43d6f4a9a1
Step 8/19 : WORKDIR ${APP_DIR}
 ---> Using cache
 ---> 1627abfc9366
Step 9/19 : COPY pyproject.toml poetry.lock ./
 ---> Using cache
 ---> f39a43de290f
Step 10/19 : RUN python -m venv --copies ${APP_DIR}/venv
 ---> Using cache
 ---> 4062a1611577
Step 11/19 : COPY ./ ./venv
 ---> b46a64464087
Step 12/19 : RUN . ${APP_DIR}/venv/bin/activate && poetry install --no-dev
 ---> Running in d14bf8f04174
Installing dependencies from lock file

Package operations: 29 installs, 0 updates, 0 removals

  • Installing idna (3.3)
  • Installing sniffio (1.2.0)
  • Installing anyio (3.6.1)
  • Installing numpy (1.22.4)
  • Installing pyparsing (3.0.9)
  • Installing typing-extensions (4.2.0)
  • Installing wrapt (1.14.1)
  • Installing asgiref (3.5.2)
  • Installing async-timeout (4.0.2)
  • Installing certifi (2022.5.18.1)
  • Installing charset-normalizer (2.0.12)
  • Installing click (8.1.3)
  • Installing deprecated (1.2.13)
  • Installing h11 (0.13.0)
  • Installing joblib (1.1.0)
  • Installing packaging (21.3)
  • Installing pydantic (1.9.1)
  • Installing pytz (2022.1)
  • Installing scipy (1.8.1)
  • Installing starlette (0.19.1)
  • Installing threadpoolctl (3.1.0)
  • Installing urllib3 (1.26.9)
  • Installing zope.interface (5.4.0)
  • Installing datetime (4.4)
  • Installing fastapi (0.78.0)
  • Installing redis (4.3.3)
  • Installing requests (2.27.1)
  • Installing scikit-learn (1.1.1)
  • Installing uvicorn (0.17.6)
Removing intermediate container d14bf8f04174
 ---> 419f1a5c1615
Step 13/19 : FROM python:3.10-slim-buster as run
 ---> d82a8f78877e
Step 14/19 : ARG APP_DIR
 ---> Using cache
 ---> d58c47c39f2f
Step 15/19 : COPY --from=build ${APP_DIR}/venv ${APP_DIR}/venv/
 ---> 11c27cb4202a
Step 16/19 : ENV PATH ${APP_DIR}/venv/bin:$PATH
 ---> Running in 862ee8f3ec7e
Removing intermediate container 862ee8f3ec7e
 ---> 14f5033e5401
Step 17/19 : COPY  . ./
 ---> eaa21fd3b886
Step 18/19 : HEALTHCHECK --start-period=30s CMD python -c "import requests; requests.get('http://localhost:8000/health', timeout=2)"
 ---> Running in cf200c8723d2
Removing intermediate container cf200c8723d2
 ---> 403769bfb023
Step 19/19 : CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
 ---> Running in 73ade661293b
Removing intermediate container 73ade661293b
 ---> d53dde525ca6
Successfully built d53dde525ca6
Successfully tagged w255_lab3_don_irwin:latest
kubectl delete -f deployment-pythonapi.yaml
kubectl delete -f deployment-redis.yaml
kubectl delete -f service-redis.yaml
kubectl delete -f service-prediction.yaml
kubectl delete -f namespace.yaml
kubectl create -f namespace.yaml
namespace/w255 created
kubectl apply -f deployment-redis.yaml
deployment.apps/redisserver created
kubectl apply -f service-redis.yaml
service/redis created
kubectl apply -f deployment-pythonapi.yaml
deployment.apps/pythonapi created
kubectl apply -f service-prediction.yaml
service/frontend created
my_all_pods=10
my_all_pods=10
my_all_pods_after_deploy=12
*********************************
*  ENDING                       *
* Docker stopping and rebuild   *
*                               *
*********************************
**********************************
*  STARTING                      *
* port forwarding                *
*                                *
* Make sure all pods are running *
* Before issuing port forwarding *
*                                *.
**********************************
/data/school/MIDS/w255/ucb_githubs/summer22-Tuneman7/lab_3/lab3
12
10
kubectl port-forward -n w255 service/frontend 8000:8000 > output.txt &
*********************************
*  ENDING                       *
* port forwarding               *
*                               *
*********************************
*********************************
*                               *
*        WAITING. ....          *
*        API not ready          *
*                               *
*********************************
*********************************
*                               *
*        API is ready           *
*                               *
*********************************


*********************************
*                               *
*     Running CURL Calls        *
*                               *
*  Note that FASTAPI uses 307   *
*  internal redirects for its   *
*  query string parsing unless  *
*  the request is formed line   *
*     /hello/?name=Don          *
*                               *
*********************************
About to call the following URI: http://localhost:8000/health
"healthy"
the return code is : 200
About to call the following URI: http://localhost:8000/hello/?name=Don
"hello Don"
the return code is : 200
About to call the following URI: http://localhost:8000/hello/?nam=Don
{"detail":[{"loc":["query","name"],"msg":"field required","type":"value_error.missing"}]}
the return code is : 422
About to call the following URI: http://localhost:8000/
the return code is : 404
{"detail":"Not Implemented"}
About to call the following URI: http://localhost:8000/docs
the return code is : 200

About to call the following URI: http://localhost:8000/hello?name=Don

the return code is : 307

*********************************
*                               *
* Posts to predict -- should    *
* have 200 return codes         *
*********************************
*********************************
* Posts to predict -- should    *
* have 200 return codes         *
* We are doing 200 iterations   *
*********************************
*********************************
* END OF GOOD 200 ZONE          *
* Posts to predict -- should    *
* have 200 return codes         *
*********************************
good_return_codes=5000
bad_return_codes=0
*********************************
* BEGINNING OF BAD ZONE         *
* Posts to predict -- should    *
* NOT have 200 return codes     *
*********************************
*********************************
* END OF BAD ZONE               *
* Posts to predict -- should    *
* NOT have 200 return codes     *
*********************************
good_return_codes=5000
bad_return_codes=5
*********************************
*                               *
*        End of bash handling   *
*                               *
*********************************
*********************************
*  KILLING                      *
* Docker stopping and remove    *
*                               *
* Stopping Kubernetes           *
*                               *
*********************************
docker stop w255_lab3_don_irwin
docker rm w255_lab3_don_irwin
kubectl delete -f deployment-pythonapi.yaml
deployment.apps "pythonapi" deleted
kubectl delete -f deployment-redis.yaml
deployment.apps "redisserver" deleted
kubectl delete -f service-redis.yaml
service "redis" deleted
kubectl delete -f service-prediction.yaml
service "frontend" deleted
kubectl delete -f namespace.yaml
namespace "w255" deleted
✋  Stopping node "minikube"  ...
🛑  Powering off "minikube" via SSH ...
🛑  1 node stopped.
*********************************
*   End of Event Pitching      *
*********************************
*********************************
*   Expected                    *
*********************************
good_return_codes=5000
bad_return_codes=5
*********************************
*   Actual                      *
*********************************
good_return_codes=5000
bad_return_codes=5
*********************************
*   RETURN CODE COUNT           *
*                               *
*   MATCH: Good                 *
*                               *
*********************************

```
5.   Additional Checks:

   - Open a browser at the following address (should not be available since docker was taken down) :   
     http://localhost:8000/hello/?name=Don
   - Look at running docker images :
   docker -ps   
   should display not display an image named *don_irwin:
```{text}
CONTAINER ID   IMAGE                 COMMAND                  CREATED         STATUS         PORTS                    NAMES

```
   - kubectl should be shut down


6.  Github Pull Request Actions:

   - View the pull request action which have been triggered.
   ![alt text](https://github.com/UCB-W255/summer22-Tuneman7/blob/main/lab_3/lab3/test_actions_results.png?raw=true)
   ![alt text](https://github.com/UCB-W255/summer22-Tuneman7/blob/main/lab_3/lab3/test_actions_detail.png?raw=true)
