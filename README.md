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
We therefore opted to build the app from scratch by exporting and building on a python 3.12 base image, isntalling the required packages etc. This makes the build times a bit longer (few mins) but lead to a lot of flexibility. Everything can be configured in the deployment files and the run.sh script that is the entry point:

All that needs to be done to start is to supply your API keys in a secrets.yaml and the configmap.yaml. (And of course create a cluster for K8s /  setup minikube)

- configmap.yaml --> Applies config maps
- fastapi-deployment.yaml --> Deploys FastAPI app
- jaeger-deployment.yaml --> Deploys Jaeger tracing (included in the project for future work, but right now not utilized or evaluated.)
- namespace.yaml --> Creates the Kubernetes namespace "haystack-app"
- ollama-deployment.yaml --> Deploys Ollama
- **run.sh -> shell script that runs the entire deployment, including indexing, serving the API and pulling any necessary models. Certain Configs can be set at the top (such as Imagename and where to push/pull it, as well as model name (should be handled outside of shellscript in future implementation)** Port forwards for jaeger as well, this is part of future work/outlook. OpenLLmetry seems to suffice for our purposes for now. 

## Implementation
The implementation of Haystack and Ollama was done in a separate Kubernetes cluster to ensure flexibility, fault-resistance and logical separation of functionalities. The Weaviate and OpenLLMetry components operate in the cloud as SaaS and have to be called outside the cluster.

### Step by step guide to start app
1. Create clusters and nodes (eg. on GKE)
Create a cluster with nodes of at least the RAM requirement of the deployed Ollama Model + 2GB of overhead (recommend 8GB). No Need for GPU, although it speeds up calls by a lot.
2. Create Weaviate and Traceloop account and retrieve keys
Get the keys for the SaaS' we use. Paste in secrets.yml after b64 encoding them. 
3. Configure additional secrets and keys
Make sure that all the required keys, urls and other config such as modelname is set in the configmap.yml and secrets.yml files.
- Configure model and image name in run.sh
modelname should fit the internal config value, can do by retrieving from env too. Fix this redundancy in future work.
- If changes occur in the environment, generate a requirements.txt for run.sh from pyproject.toml/uv.lock file
- Call run.sh
Optional for testing with external calls on API on a small streamlit GUI:
- Configure API URL in sample_app.py
- Execute streamlit run sample.py

### On Ollama
The Ollama (https://ollama.com/) setup in our Kubernetes deployment is configured to run any given model as the primary LLM for the RAG pipeline, depending on available resources you have to choose an appropriate one. Ollama is containerized using the official ollama/ollama:latest image and deployed as a Kubernetes service (ollama-deployment.yaml). Once the deployment is active, the system pulls the specified model inside the running container to ensure it is available for inference (in the run.sh). The service is accessible within the cluster at http://ollama:11434, allowing seamless integration with Haystack for processing queries.


### Vector Database Sample Data
To provide the LLM with data, this system uses Weaviate (https://weaviate.io/) as a vector database. The additional information is stored as a list of strings, for example:

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
This is ofcourse only example content, both the database content and complexity of the pipeline need to be aapted for real world usecases.

### Tracing Setup
The tracking service in our Kubernetes deployment is powered by OpenLLMetry (https://www.traceloop.com/docs/openllmetry/introduction), providing observability for the RAG pipeline. OpenLLMetry collects and exports telemetry data, including traces and metrics. OpenLLMetry instrumentation is integrated into the FastAPI and Haystack services to capture traces and logs automatically. It provides the following Insights:
- A Dashboard that shows an overview of
    - Models
    - Price Total
    - Dauily Cost
    - Number Requests
    - Tokens Amount that were used over time
    - A Median Latency
 
  it additionally allows to add further metrics on custom dashboards, depending on your traces.

- A tracing tab that allows evaluaton of all spans that were captured, as well as a drill down intp specific spans with Token count, latency, timestamps and the model used.

The following Results contain exemplary images of these views.

## Results
As seen in the screenshots below, the FastAPI interface allows to send a specified query to the LLM which responds with a generated response suited to the given query. 

![Results General Knowledge](https://raw.githubusercontent.com/phigep/clc3-rag-tracing/refs/heads/main/result-general.png)

When asked a general question, as for the capital city of France, the LLM generates its own response, without the additional information stored in the vector database.

![Results Vector DB Knowledge](https://raw.githubusercontent.com/phigep/clc3-rag-tracing/refs/heads/main/result-fruits.png)

When asked a specific question regarding the information in the vector database, this information is retreived from the document objects, in order to generate a good response.

### Tracing with OpenLLMetry

**Dashboard**
![image](https://github.com/user-attachments/assets/3fcf4e70-6087-4e49-96f3-df0c5822fe43)
As previously mentioned, it shows an overview of relevant operational LLM/RAG metrics. As we only use ollama and local deployment, no costs are incurred for any SaaS models (openai, anthropic etc.)

**Single Trace/Span**
![image](https://github.com/user-attachments/assets/bd674ed5-e4d8-4094-aebf-4a35b5a0f497)

With the following data on the LLMs:
![image](https://github.com/user-attachments/assets/795f998c-bdbe-41fa-97aa-0da7bea4e9fe)

This together with the details panel that shows duration of call etc, is enough to evaluate the performance of our RAG pipeline form an operational point of view. It allows for evaluation of different models, based on their speed and allows a non aggregated evaluation of quality, reasoning capabilities (with the answer). As an example we also show a contrasting run with deepseek-r1 style model based on qwen-2:

![image](https://github.com/user-attachments/assets/bb7b7a8c-9f7c-41e7-840b-acab83de0729)

As we can see, it takes much longer but also does some very impressive reasoning. it ignores useless context that was provided but also takes over 80s to generate an answer. 

Note: Performance is not representative of a real use, as only CPU based inference was done to save credits on GCloud. 

## Lessons Learned and Outlook
The here shown prototype works well in limited scope but taught us a few lessons in terms of documentation quality and in particular potential issues when using a package that is quite new and limited. Although Haystack itself works quite well in local settings, when deploying it with the recommended way of using their custom hayhooks image and approach, inconsistencies across the integrations and documentation of examples set us up for failure. We therefore had to do a lot more from scratch for the RAG deployment itself, leaving us less time for the tracing. The tracing on the other hand is, based on OpenTelemetry -> OpenLLMetry incredibly simple to get started on a basic level. This was a very positive learning which will lead to (hopefully) an open approach to tracing for us. Keeping the image lightweight enough to rebuild often also was a learning. 

We also learned that logging and kubectl logs command are your best friend when trying to debug the deployment, the immutable and readonly nature of how kubernetes pulls the images and rebuilds, forced us to solve problems at the root (our image), without any big changes to the deployed system. 

Secrets and Configmap was also a critical learning, as multiple potentially costly API Keys can and are used for this project. We initially started with a .env file but quickly realized that this wont be an option for the actual deployment.

### Outlook
There are a lot of areas with room for improvement, we only name a few here. It has to e understood that this is a simple prototype using the most basic approaches to cut down on coding effort a bit.
- RAG Pipeline: Improve on the basic Pipeline and present the RAG functionality as a tool call instead. Use Embedding and Hybrid Retrieval for better results.
- Evaluation and Tracing: To the impressive and useful OpenLLMetry traces, add some custom tracing for e.g. RAG metrics on startup (RAGAS)
- Deployment and Model Pulling: use a single point of truth that is configurable easy in the run.sh if possible for the modelname, or alternatively keep the future API flexible enough to choose the name. Right now there is some redundancy with the configmap name for the API and the model thats pulled in the run.sh script. Maybe Ollama has a setting that automatically pulls a model on first request.
- Less SaaS: Weaviate can also be easily deployed on a Pod, this will however accrue additional costs, which we avoided with the free weaviate cloud version for now. 



