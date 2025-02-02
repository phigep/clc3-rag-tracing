#!/bin/bash

# Set script to exit on error if any command fails
set -e

# Define variables
IMAGE_NAME="phigep/haystack-pipeline"
IMAGE_TAG="latest"
OLLAMA_IMAGE="ollama/ollama:latest"
NAMESPACE="haystack-app"
OLLAMA_MODEL="llama3.1"

echo "🚀 Starting Kubernetes Deployment for FastAPI, Ollama, OpenTelemetry & Jaeger..."

echo "📌 Creating Kubernetes Namespace ($NAMESPACE)..."
kubectl apply -f namespace.yaml

echo "🔐 Applying Secrets..."
kubectl apply -f secrets.yaml

echo "🛠️ Applying ConfigMaps..."
kubectl apply -f configmap.yaml

echo "🐳 Building Docker image: $IMAGE_NAME:$IMAGE_TAG..."
podman build --arch amd64 -t $IMAGE_NAME:$IMAGE_TAG .

# 2️⃣ Push the FastAPI Image to DockerHub
echo "📤 Pushing Docker image to DockerHub..."
podman push $IMAGE_NAME:$IMAGE_TAG

# 3️⃣ Deploy Kubernetes Configurations

echo "📌 Applying ConfigMaps and Secrets..."
kubectl apply -f jaeger-deployment.yaml
kubectl apply -f ollama-deployment.yaml  # ✅ Deploy Ollama

echo "📌 Deploying FastAPI App..."
kubectl apply -f fastapi-deployment.yaml

# 4️⃣ Restart Deployments to Pull Latest Images
echo "🔄 Restarting FastAPI Deployment..."
kubectl rollout restart deployment/haystack-app -n $NAMESPACE

echo "🔄 Restarting Ollama Deployment..."
kubectl rollout restart deployment/ollama -n $NAMESPACE

# 5️⃣ Verify Deployment Status
echo "📡 Waiting for pods to be ready..."
kubectl wait --for=condition=available deployment/haystack-app -n $NAMESPACE --timeout=120s
kubectl wait --for=condition=available deployment/ollama -n $NAMESPACE --timeout=120s

echo "✅ All services deployed successfully!"

# 6️⃣ Get Service Details
kubectl get svc -n $NAMESPACE

echo "🎯 FastAPI should be accessible at:"
echo "🌍 http://$(kubectl get svc -n $NAMESPACE haystack-app -o jsonpath='{.status.loadBalancer.ingress[0].ip}')/docs"

echo "🎯 Ollama should be accessible inside the cluster at:"
echo "🌍 http://ollama:11434"


echo "🛠️ Pulling Ollama Model ($OLLAMA_MODEL) in the container..."

# Get the pod name dynamically
OLLAMA_POD=$(kubectl get pods -n $NAMESPACE -l app=ollama -o jsonpath='{.items[0].metadata.name}')

# Check if the pod name was found
if [ -z "$OLLAMA_POD" ]; then
  echo "❌ Error: No Ollama pod found in namespace $NAMESPACE"
  exit 1
fi

# Run the command inside the pod
kubectl exec -n $NAMESPACE $OLLAMA_POD -- ollama pull $OLLAMA_MODEL

echo "✅ Ollama Model ($OLLAMA_MODEL) is downloaded and ready!"


# 7️⃣ Port-forward Jaeger UI for local access
echo "📡 Access Jaeger UI at http://localhost:16686"
kubectl port-forward -n $NAMESPACE svc/jaeger 16686:16686 &

echo "🎯 All systems are up and running!"
