# clc3-rag-tracing
This repo contains all the information and code for our semester project in cloud computing.

## What is the high-level goal of your project?
The high level goal of our project is a retrieval-augmented generation pipeline (prototypical) that runs on kubernetes with included tracing of requests, retrieved contexts and generated answers. It should allow for local LLMs to be used (vLLM), which might help with scalability and security. 
A scalable and understandable (tracing!) RAG pipeline helps in refining the retrieval **and** generation part. 

## Cloud Architecture
![Haystack Pipeline](https://github.com/user-attachments/assets/cf6e5b7f-f0c6-4bd6-ac79-82a8a82027ce)

## Implementation
The implementation of every single component in this architecture was done in a separate Kubernetes cluster to ensure flexibility, fault-resistance and logical separation of functionalities.

### Haystack Setup


### Ollama Setup


### LLM Selection
We selected the 1.5B Qwen model for our RAG-based Kubernetes setup due to its optimal balance between performance and resource efficiency. With a relatively small parameter size, it offers solid language understanding and generation capabilities while remaining lightweight enough for deployment in a containerized environment. This ensures efficient resource utilization, minimizing GPU and memory consumption without significantly sacrificing response quality. Additionally, Qwen’s architecture integrates well with our retrieval-augmented generation (RAG) pipeline, allowing for fast, contextually relevant responses. However, we are also cautious about the censorship mechanisms embedded in the model by the Chinese government, which introduce biases and restrict certain outputs. This concern requires careful evaluation and potential mitigations to ensure that the model aligns with our system’s requirements for open and unbiased information retrieval.

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


## Results



