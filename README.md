<h1> cloudProjectIris </h1>
<h3> Project on Google Cloud Platform (GCP) focused on learning how to use Docker and Kubernetes, how to expose Flask Applications and how to separate different tasks when deploying a simple ML model as a structure of microservices: </h3>

- [**Frontend**](./frontend5000) --> The only service with Public IP with which the user can interact.
- [**Backend**](./backend8080) --> Handles the connections with the database and the Machine Learning model.
- [**Mysql**](./mysql3306) --> Serves as a Database that stores the predictions of the Machine Learning model.
- [**Model**](./irismodel3000) --> Pretrained ML model on the [Iris dataset](https://www.kaggle.com/datasets/uciml/iris)

<h4> How to run on Docker: </h4>

1. `docker network create cloudprojectiris`
2. `docker run -d --name mysql --net cloudprojectiris victorrgez/cloudprojectirismysql`
3. `docker run -d --name model --net cloudprojectiris victorrgez/cloudprojectirismodel`
4. `docker run -d -p=0.0.0.0:5000:5000 --name frontend --net cloudprojectiris victorrgez/cloudprojectirisfrontend`
5. `docker run -d --name backend --net cloudprojectiris victorrgez/cloudprojectirisbackend`
6. Visit http://localhost:5000 or copy the external IP of your machine instead of `localhost`

<h4> How to stop on Docker: </h4>

1. `docker stop backend frontend model mysql`
2. `docker rm backend frontend model mysql`
3. Remove the images individually with `docker rmi` (you can list them with `docker image ls`)
4. `docker network rm cloudprojectiris`

<h4> How to run on Docker-Compose: </h4>

1. `git clone https://github.com/victorrgez/cloudprojectiris.git`
2. `cd cloudprojectiris`
3. `docker-compose up -d`

<h4> How to stop on Docker-Compose: </h4>

<h6> a/ If you want to remove the database: </h6>

1. `docker-compose down -v`

<h6> b/ If you want to keep the database: </h6>

1. `docker-compose down`

<h4> How to run on Kubernetes: </h4>

1. `git clone https://github.com/victorrgez/cloudprojectiris.git`
2. Install `kompose.io` following the instructions for your OS https://kompose.io/installation/
3. `cd cloudprojectiris`
4. `kompose convert -f docker-compose.yml`
5. Add `type: LoadBalancer` inside the `spec` block in the file `frontend-service.yaml` like in [here](./kubernetesYAMLFiles/frontend-service.yaml)
6. `kubectl apply -f .` (ignore warnings about docker-compose.yml)
7. Wait a couple of minutes for `mysql` service to start-up so that `backend` can eventually become healthy
8. `kubectl get service frontend`
9. Copy the `EXTERNAL-IP` in your browser and put `:5000` at the end

Alternatively you can run `kubectl apply -f .` inside the `kubernetesYAMLFiles` folder instead of using `kompose.io`

<h4> How to stop on Kubernetes: </h4>

1. `kubectl delete services frontend backend mysql model`
2. `kubectl delete deployments frontend backend mysql model`
3. `kubectl delete pvc statefuldatabase`
