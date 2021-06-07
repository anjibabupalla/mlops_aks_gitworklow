mlops_aks
==============================

migrate existing ml to azure devops and deploy to aks

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>


dvc commands (not able to connect need to explore)
```bash
pip install dvc
dvc init
dvc remote add myremote https://mlopsdatasets.blob.core.windows.net/winequality-data
git add .dvc/config && git commit -m "Configure remote storage"
dvc remote default myremote
dvc push
```

setting docker registry to minikube (https://medium.com/swlh/how-to-run-locally-built-docker-images-in-kubernetes-b28fbc32cc1d)
```bash
minikube docker-env
export DOCKER_TLS_VERIFY=”1"
export DOCKER_HOST=”tcp://172.17.0.2:2376"
export DOCKER_CERT_PATH=”/home/user/.minikube/certs”
export MINIKUBE_ACTIVE_DOCKERD=”minikube”
# To point your shell to minikube’s docker-daemon, run:
eval $(minikube -p minikube docker-env)
```

how to push docker images into docker hub
==========================================
      docker build -f /path/to/mydockerfile -t <new image name> .
         docker build -f Dockerfile -t mlopsazure .
        create an account in hub.docker.com
                create a reportsitory after logged into the account (ex: myapp)
      
                on docker host
                docker login
                        username: docker hub username
                        password: docker hub passwd
                ensure you get "Login Succeeded" message

                docker tag local-image:tagname new-repo:tagname
                    docker tag mlops_aks mlops_aks:v1
                docker push new-repo:tagname
                     docker push mlops_aks:v1


push to docker hub
```bash
docker build --tag mlops_aks .
docker run mlops_aks
docker run --publish 5000:5000 mlops_aks
or
docker run -it -d -p 5000:5000 anjibabupalla/mlops_aks:v1
docker push anjibabupalla/mlops_aks:v1
