# clc3-rag-tracing
This repo contains all the information and code for our semester project in cloud computing.

## What is the high-level goal of your project?

The high level goal of our project is a retrieval-augmented generation pipeline (prototypical) that runs on kubernetes with included tracing of requests, retrieved contexts and generated answers. It should allow for local LLMs to be used (vLLM), which might help with scalability and security. 
A scalable and understandable (tracing!) RAG pipeline helps in refining the retrieval **and** generation part. 

## What will we newly build and develop? What does already exist?
We will be using Haystack as a central component for our architecture. This open source AI framework handles the communication in our system. We will have to configure and set it up. Additionally, the interface to the other components will have to be configured. Haystack will also serve as a central entry point for the end-user.
We will select an LLM model, which will be hosted in vLLM. We will configure vLLM to forward prompts to this LLM model and return responses.
We have not yet decided on which exact vector database we will use, but Weaviate might be a candidate. After deciding on one of them, we will have to set it up in Kubernetes, define the collection, populate it and connect it to Haystack. 
We will configure and setup OpenLLMetry in a separate Kubernetes pot. It will need integration with Haystack in order to get notified when certain events happen.
Using Kubernetes, we can set this whole project up in a cloud environment. Different clusters will be configured in order to strucuter the project in separate entities and split up the workload and resource usage.

## How does it relate to Cloud-Computing? What cloud technologies are we using?
The architecture of our project is based on Kubernetis. We plan on operating the relevant components of our projects in different Kubernetis pots and connecting them within the cloud. The cloud architecture can be seen in the diagram above. The OpenLLMetry component will be observing the rest of the system throughout the entire cloud architecture.

## How does the high-level cloud architecture look like? Provide an architecture diagram. 
![Haystack Pipeline](https://github.com/user-attachments/assets/cf6e5b7f-f0c6-4bd6-ac79-82a8a82027ce)



## Some Links for Research
https://github.com/traceloop/openllmetry/tree/main
https://medium.com/@ronen.schaffer/follow-the-trail-supercharging-vllm-with-opentelemetry-distributed-tracing-aa655229b46f
https://docs.dynatrace.com/docs/analyze-explore-automate/dynatrace-for-ai-observability/sample-use-cases/self-service-ai-observability-tutorialhttps://haystack.deepset.ai/integrations/vllm
https://docs.haystack.deepset.ai/docs/kubernetes
https://haystack.deepset.ai/integrations/traceloop
