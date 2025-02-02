# CLC3 Project: Traced RAG Pipeline on K8s
This repository contains all the information and code for our semester project in cloud computing.

## What is the high-level goal of our project?
The high level goal of our project is a retrieval-augmented generation pipeline (prototypical) that runs on kubernetes with included tracing of requests, retrieved contexts and generated answers. It should allow for local LLMs to be used (vLLM), which might help with scalability and security. 
A scalable and understandable (tracing!) RAG pipeline helps in refining the retrieval and generation part. 
## Project Structure
**src/backend** contains the API that is the final "product" and exposed to the outside. 
The project root contains the deployment files (see below) as well as the Dockerfile that is used to build the image we use (phigep/haystack-pipeline). 

We build a custom image for the python project instead of the hayhooks image. (Reasons see deployment). 

The project itself uses **python 3.12 and uv** as pmanager. If new packages are added to this prototype during further implementation, a requirements.txt needs to be exportet from the pyproject.toml!  

## Cloud Architecture
![Haystack Pipeline](https://raw.githubusercontent.com/phigep/clc3-rag-tracing/refs/heads/main/architecture.png)
The parts of our system are as follows:
- Ollama Container that run an Ollama Server (https://ollama.com), which serves the used model.  
- Rest API Container that runs a small exemplary RAG pipeline with Haystack (https://haystack.deepset.ai) with a single GET Call on a FASTAPI as entry point.
  Uses the Ollama Model and the Weaviate SaaS database. Uses BM25 retrieval.  
- Connection to SaaS Vector Database (Weaviate) and SaaS LLM tracing (OpenLLMetry) based on Opentelemetry. 


### Deployment Files
Haystack recommends using hayhooks for deploying on K8s. However, this package has seen breaking changes in the recent past, is not particularly well documented (quite horribly tbh) and most importantly fails when trying to deploy Pipelines that contain pydantic models or **even some of haystacks own integrations (weaviate, ollama)**. 
All that needs to be done to start is to supply your API keys in a secrets.yaml and the configmap.yaml. (And of course create a cluster for K8s /  setup minikube)

- configmap.yaml --> Applies config maps
- fastapi-deployment.yaml --> Deploys FastAPI app
- jaeger-deployment.yaml --> Deploys Jaeger tracing (included in the project for future work, but right now not utilized or evaluated.)
- namespace.yaml --> Creates the Kubernetes namespace "haystack-app"
- ollama-deployment.yaml --> Deploys Ollama
- run.sh -> shell script that runs the entire deployment, including indexing, serving the API and pulling any necessary models. 

## Implementation
The implementation of Haystack and Ollama was done in a separate Kubernetes cluster to ensure flexibility, fault-resistance and logical separation of functionalities. The Weaviate and OpenLLMetry components operate in the cloud and have to be called outside the cluster.

### Step by step guide
- Create clusters and nodes on GKE
- Create Weaviate and Traceloop account and retreive keys
- Configure secrets and keys
- Configure model and image name in run.sh
- If changes occur in the environment, generate a requirements.txt for run.sh
- Call run.sh
- Configure API URL in sample_app.py
- Execute streamlit run

### Haystack Setup
The Haystack (https://haystack.deepset.ai/) setup in our Kubernetes deployment is designed to integrate seamlessly with FastAPI, Ollama, OpenLLMetry, and Jaeger for efficient retrieval-augmented generation (RAG). The deployment process begins by creating a dedicated Kubernetes namespace and applying necessary secrets and configuration maps. The core Haystack pipeline is containerized as a Docker image, which is built, pushed to DockerHub, and deployed in the cluster. The Ollama service is deployed alongside it to handle LLM-based responses. Once the deployments are up, they are restarted to pull the latest images, and the system waits for all services to become available. The setup also includes monitoring and tracing with Jaeger, accessible via port forwarding, ensuring full observability of the pipeline.

### Ollama Setup
The Ollama (https://ollama.com/) setup in our Kubernetes deployment is configured to run any given model as the primary LLM for the RAG pipeline. The deployment starts by creating a dedicated namespace and applying necessary secrets and configuration maps. Ollama is containerized using the official ollama/ollama:latest image and deployed as a Kubernetes service (ollama-deployment.yaml). Once the deployment is active, the system pulls the specified model inside the running container to ensure it is available for inference. The service is accessible within the cluster at http://ollama:11434, allowing seamless integration with Haystack for processing queries. Additionally, the deployment includes automated restarts to ensure the latest updates are applied and proper health checks to verify availability.

### LLM Selection
We selected the 1.5B Qwen model for our RAG-based Kubernetes setup due to its optimal balance between performance and resource efficiency. With a relatively small parameter size, it offers solid language understanding and generation capabilities while remaining lightweight enough for deployment in a containerized environment. This ensures efficient resource utilization, minimizing GPU and memory consumption without significantly sacrificing response quality. Additionally, Qwen’s architecture integrates well with our retrieval-augmented generation (RAG) pipeline, allowing for fast, contextually relevant responses. However, we are also cautious about the censorship mechanisms embedded in the model by the Chinese government, which introduce biases and restrict certain outputs. This concern requires careful evaluation and potential mitigations to ensure that the model aligns with our system’s requirements for open and unbiased information retrieval.

### Vector Database Setup
To provide the LLM with additional data, this system uses Weaviate (https://weaviate.io/) as a vector database. The additional information is stored as a list of strings, for example:

`
list_of_strings = [
    "Emily has 14 of apples",
    "Michael has 83 of oranges",
    "Sophia has 27 of grapes"
]
`

By converting this list of strings into a list of document objects, Weaviate can efficiently provide the RAG pipeline with the supplementary data:

`
docs = [Document(content=x) for i,x in enumerate(list_of_strings)]
`

### Tracing Setup
The tracking service in our Kubernetes deployment is powered by OpenLLMetry (https://www.traceloop.com/docs/openllmetry/introduction), providing observability for the RAG pipeline. OpenLLMetry collects and exports telemetry data, including traces and metrics. OpenLLMetry instrumentation is integrated into the FastAPI and Haystack services to capture traces and logs automatically. This setup ensures real-time tracking, performance analysis, and debugging capabilities for the entire pipeline.

## Results
As seen in the screenshots below, the FastAPI interface allows to send a specified query to the LLM which responds with a generated response suited to the given query. 

![Results General Knowledge](https://raw.githubusercontent.com/phigep/clc3-rag-tracing/refs/heads/main/result-general.png)

When asked a general question, as for the capital city of France, the LLM generates its own response, without the additional information stored in the vector database.

![Results Vector DB Knowledge](https://raw.githubusercontent.com/phigep/clc3-rag-tracing/refs/heads/main/result-fruits.png)

When asked a specific question regarding the information in the vector database, this information is retreived from the document objects, in order to generate a good response.



