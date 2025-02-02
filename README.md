# clc3-rag-tracing
This repo contains all the information and code for our semester project in cloud computing.

## What is the high-level goal of our project?
The high level goal of our project is a retrieval-augmented generation pipeline (prototypical) that runs on kubernetes with included tracing of requests, retrieved contexts and generated answers. It should allow for local LLMs to be used (vLLM), which might help with scalability and security. 
A scalable and understandable (tracing!) RAG pipeline helps in refining the retrieval **and** generation part. 

## Cloud Architecture
![Haystack Pipeline](https://github.com/user-attachments/assets/cf6e5b7f-f0c6-4bd6-ac79-82a8a82027ce)

## Implementation
The implementation of every single component in this architecture was done in a separate Kubernetes cluster to ensure flexibility, fault-resistance and logical separation of functionalities.

### Haystack Setup
The Haystack (https://haystack.deepset.ai/) setup in our Kubernetes deployment is designed to integrate seamlessly with FastAPI, Ollama, OpenTelemetry, and Jaeger for efficient retrieval-augmented generation (RAG). The deployment process begins by creating a dedicated Kubernetes namespace and applying necessary secrets and configuration maps. The core Haystack pipeline is containerized as a Docker image (phigep/haystack-pipeline:latest), which is built, pushed to DockerHub, and deployed in the cluster. The Ollama service, running the 1.5B Qwen model, is deployed alongside it to handle LLM-based responses. Once the deployments are up, they are restarted to pull the latest images, and the system waits for all services to become available. The setup also includes monitoring and tracing with Jaeger, accessible via port forwarding, ensuring full observability of the pipeline.

### Ollama Setup
The Ollama (https://ollama.com/) setup in our Kubernetes deployment is configured to run the 1.5B Qwen model as the primary LLM for the RAG pipeline. The deployment starts by creating a dedicated namespace and applying necessary secrets and configuration maps. Ollama is containerized using the official ollama/ollama:latest image and deployed as a Kubernetes service (ollama-deployment.yaml). Once the deployment is active, the system pulls the specified model (qwen2:1.5B) inside the running container to ensure it is available for inference. The service is accessible within the cluster at http://ollama:11434, allowing seamless integration with Haystack for processing queries. Additionally, the deployment includes automated restarts to ensure the latest updates are applied and proper health checks to verify availability.

### LLM Selection
We selected the 1.5B Qwen model () for our RAG-based Kubernetes setup due to its optimal balance between performance and resource efficiency. With a relatively small parameter size, it offers solid language understanding and generation capabilities while remaining lightweight enough for deployment in a containerized environment. This ensures efficient resource utilization, minimizing GPU and memory consumption without significantly sacrificing response quality. Additionally, Qwen’s architecture integrates well with our retrieval-augmented generation (RAG) pipeline, allowing for fast, contextually relevant responses. However, we are also cautious about the censorship mechanisms embedded in the model by the Chinese government, which introduce biases and restrict certain outputs. This concern requires careful evaluation and potential mitigations to ensure that the model aligns with our system’s requirements for open and unbiased information retrieval.

### Vector Database Setup
To enhance the RAG pipeline with additional data, this system uses Weaviate (https://weaviate.io/) as a vector database. The additional information is stored as a list of strings, for example:

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
The tracking service in our Kubernetes deployment is powered by OpenTelemetry (https://opentelemetry.io/) and Jaeger (https://www.jaegertracing.io/), providing observability for the RAG pipeline. OpenTelemetry collects and exports telemetry data, including traces and metrics, while Jaeger enables distributed tracing to monitor requests across services. The setup begins by deploying Jaeger using jaeger-deployment.yaml, ensuring it runs as a dedicated service within the cluster. OpenTelemetry instrumentation is integrated into the FastAPI and Haystack services to capture traces and logs automatically. To facilitate local monitoring, port forwarding is enabled, making the Jaeger UI accessible at http://localhost:16686. This setup ensures real-time tracking, performance analysis, and debugging capabilities for the entire pipeline.
