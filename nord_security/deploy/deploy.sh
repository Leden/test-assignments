# This script will build and deploy the app into the local minikube cluster.
# Make sure to have `.env` file ready before running this script.
# See comments in `.env.example` for help.

# Verify `.env` file exists
[ -f ".env" ] || {
    echo "Fail: .env file is missing."
    exit 1
}

# Determine current script directory
dir=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)

# Configure `docker` command to talk to the minikube Docker runtime
eval $(minikube docker-env)

# Build the app image
docker build . -t weatherapi

# Apply namespace manifest
minikube kubectl -- apply -f "$dir/namespace.yaml"

# Create secrets from `.env` file
minikube kubectl -- create secret generic weatherapi --from-env-file="$dir/../.env" --namespace=weatherapi

# Apply deployment manifest
minikube kubectl -- apply -f "$dir/deployment.yaml"

# Apply service manifest
minikube kubectl -- apply -f "$dir/service.yaml"
