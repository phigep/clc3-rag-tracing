# clc3-rag-tracing
This repo contains all the information and code for our semester project in cloud computing.

# What will we newly build and develop? What does already exist?
We will be using Haystack as a central component for our architecture. This open source AI framework handles the communication in our system. We will have to configure and set it up. Additionally, the interface to the other components will have to be configured. Haystack will also serve as a central entry point for the end-user.
We will select an LLM model, which will be hosted in vLLM. We will configure vLLM to forward prompts to this LLM model and return responses.
We have not yet decided on which exact vector database we will use, but Weaviate might be a candidate. After deciding on one of them, we will have to set it up in Kubernetis, define the collection, populate it and connect it to Haystack. 
We will configure and setup OpenLLMetry in a separate Kubernetis pot. It will need integration with Haystack in order to get notified when certain events happen.
Using Kubernetis, we can set this whole project up in a cloud environment. Different clusters will be configured in order to strucuter the project in separate entities and split up the workload and resource usage.



# How does it relate to Cloud-Computing? What cloud technologies are we using?
The architecture of our project is based on Kubernetis. We plan on operating the relevant components of our projects in different Kubernetis pots and connecting them within the cloud. The cloud architecture can be seen in the diagram above. The OpenLLMetry component will be observing the rest of the system throughout the entire cloud architecture.
