<h1> cloudProjectIris </h1>
<h3> Project on GCP focused on learning how to use Docker and Kubernetes, how to expose Flask Applications and how to separate different tasks from a simple ML app into microservices: </h3>

- [**Frontend**](./frontend5000) --> The only service with Public IP with which the user can interact.
- [**Backend**](./backend8080) --> Handles the connection with the database and the Machine Learning model.
- [**Mysql**](./mysql3306) --> Serves as a Database that stores the predictions of the Machine Learning model.
- [**Model**](./irismodel3000) --> Pretrained ML model on the [Iris dataset](https://www.kaggle.com/datasets/uciml/iris)

<h4> How to run on Docker-Compose: </h4>

1. `git clone https://github.com/vitorrgez/cloudprojectiris.git`
2. `cd cloudprojectiris`
3. `docker-compose up -d`

<h4> How to stop on Docker-Compose: </h4>

<h6> a/ If you want to remove the database: </h6>

1. `docker-compose down -v`

<h6> b/If you want to keep the database: </h6>

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

<h4> How to stop on Kubernetes: </h4>

1. `kubectl delete services frontend backend mysql model`
2. `kubectl delete deployments frontend backend mysql model`
3. `kubectl delete pvc statefuldatabase`
