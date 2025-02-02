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

## Milestones  
This section outlines the key milestones and their corresponding target completion dates.

**Milestone 1:** Exploration and Setup *(November 24, 2024)*  
- Conducted an initial brainstorming session via virtual call to explore Kubernetes, vLLM, Haystack, and vector databases.  
- Created a preliminary architecture diagram on Canvas to outline the project’s high-level structure and components.  

**Milestone 2:** Individual Research *(December 1, 2024)*  
Each team member conducts individual research on their assigned components and writes a short summary to share with the team:  
- **David:** Deep dive into vLLM and its integration capabilities with Kubernetes.  
- **Philipp:** Research on Kubernetes deployment strategies and high-level architecture optimizations.  
- **Max:** Study of Haystack pipelines and tracing solutions (e.g., OpenLLMetry) for monitoring query flow.  

**Milestone 3:** Draft Proposal Submission *(December 15, 2024)*  
- Consolidate research findings and finalize the architecture diagram for the proposal.  
- Clearly define project goals, architecture, and components in the proposal.  
- Submit the draft proposal by the deadline *(December 17, 2024)*.  

**Milestone 4:** Component Prototyping *(January 10, 2025)*  
- Begin hands-on prototyping for each component:  
   - Set up a basic Kubernetes cluster in a cloud.  
   - Deploy initial pods for the vLLM, Haystack Pipeline, and vector database.  
   - Test components to identify potential issues.  

**Milestone 5:** Integrating and Testing *(January 19, 2025)*  
- Integrate all components with the Kubernetes cluster.  
- Test communication between pods and query workflows end-to-end.  
- Incorporate OpenLLMetry for tracing and monitoring.  

**Milestone 6:** Final Presentation Preparation *(January 26, 2025)*  
- Refine deployment, address issues that may have arisen during testing, and optimize the architecture for the final presentation.  
- Prepare slides and documentation.  

**Milestone 7:** Project Presentation *(February 3, 2025)*  
- Deliver the final presentation.  

## Contribution per Team Member  

This section outlines the contributions of each team member to the project.

### **Collaborative Tasks**  
- All team members will research one major component during **Milestone 2** and participate in **integration testing** during **Milestone 5** to refine the architecture.  
- Each member will provide insights for slides and documentation.  
- Each member will participate in virtual progress check-ins to share updates and address issues.  
- Each member will test and verify the **end-to-end functionality** of the deployed architecture and record issues and challenges (*Milestone 5*).  

### **Individual Tasks**  

#### **Max**  
- Research and configure the **Haystack pipeline**.  
- Integrate the Haystack pipeline with the **vector database** and **tracing tools** (e.g., OpenLLMetry).  
- Focus on ensuring the **query flow** works seamlessly across all components.  
- Document milestones and create slides for the **final presentation**.  
   - Slides will showcase:  
     - High-level goals and architecture.  
     - Demonstration of the implemented system.  
     - Challenges faced and solutions implemented.  
     - Key learnings.  

#### **David**  
- Research and configure **vLLM** within a Kubernetes pod to simulate **OpenAI Mimic**.  
- Collaborate with Philipp to integrate **vLLM** into the Haystack pipeline.  
- Contribute to **integration testing** of vLLM with other pods.  
- Provide input for the project **proposal**.  

#### **Philipp**  
- Design and configure the **high-level cloud architecture**.  
- Set up and deploy the **Kubernetes cluster** on a cloud platform.  
- Integrate all pods (**vLLM, Haystack pipeline, vector database, tracing tools**).  
- Provide an **architecture diagram** and contribute to the high-level project goal in the proposal.  

## Some Links for Research
https://github.com/traceloop/openllmetry/tree/main
https://medium.com/@ronen.schaffer/follow-the-trail-supercharging-vllm-with-opentelemetry-distributed-tracing-aa655229b46f
https://docs.dynatrace.com/docs/analyze-explore-automate/dynatrace-for-ai-observability/sample-use-cases/self-service-ai-observability-tutorialhttps://haystack.deepset.ai/integrations/vllm
https://docs.haystack.deepset.ai/docs/kubernetes
https://haystack.deepset.ai/integrations/traceloop
