# Server Health Check Application

This application runs a web server that provides Prometheus health metrics for
two URLs:

- https://httpstat.us/503
- https://httpstat.us/200

The following metrics are provided for each URL:

*sample_external_url_up*: The availability status of the URL. A value of "1" is
given if the URL responds with HTTP 200. All other HTTP statuses will give "0".

*sample_external_url_response_ms*: The response time of the receiving a
reply from the URL. Unit is in milliseconds.

## Installation

This guide details installation of this application via Kubernetes Helm Chart
using a local Kubernetes development server (ex. minikube).

### Pre-requisites

- Kubernetes application
- helm CLI

### Installation Steps

#### Build the Docker Image

1. In this directory, run `docker build -t server-check:0.0.1 .`

2. Optionally, push this image to a repository. 

#### Deploy the Chart

1. If using minikube, execute `eval $(minikube docker-env)` to enable consuming
images from your local Docker daemon. Otherwise skip this step.

2. Navigate to `helm` directory and run `helm install ./check-server`. NOTE: If
you pushed your image to a remote repository, append:

        --set image.pullPolicy=IfNotPresent --set image.repository=<your external image>

2. The default service networking configuration defined in the chart is
ClusterIP - to access the application, run the following commands to
create a tunnel from your computer to the pod:

        export POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/name=server-chart,app.kubernetes.io/instance=test" -o jsonpath="{.items[0].metadata.name}")
        export CONTAINER_PORT=$(kubectl get pod --namespace default $POD_NAME -o jsonpath="{.spec.containers[0].ports[0].containerPort}")
        echo "Visit http://127.0.0.1:8080 to use your application"
        kubectl --namespace default port-forward $POD_NAME 8080:$CONTAINER_PORT

3. Access the Prometheus metrics by visiting http://127.0.0.1:8080

## Limitations

- This application is configured to check server URLs every 5 seconds
