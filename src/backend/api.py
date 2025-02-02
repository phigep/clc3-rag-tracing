
from haystack import Document,Pipeline
from haystack_integrations.document_stores.weaviate import WeaviateDocumentStore, AuthApiKey
from haystack_integrations.components.retrievers.weaviate.bm25_retriever import WeaviateBM25Retriever
from haystack.components.generators import OpenAIGenerator
from haystack.components.builders.prompt_builder import PromptBuilder
from dataclasses import dataclass
from haystack.components.joiners.document_joiner import DocumentJoiner 
from haystack_integrations.components.generators.ollama import OllamaGenerator
from haystack.components.builders.answer_builder import AnswerBuilder
import os
from fastapi import FastAPI, Request
import sys
from traceloop.sdk import Traceloop

Traceloop.init(app_name="haystack_app")

#from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
import os



from opentelemetry import trace
from opentelemetry.exporter import jaeger
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchExportSpanProcessor
#TODO if time!




# create pipeline and haystack stuff
# use weaviate as db
# use Ollama server for inference
list_of_strings = [
    "Emily has 14 of apples",
    "Michael has 83 of oranges",
    "Sophia has 27 of grapes",
    "Alexander has 91 of pears",
    "Evelyn has 41 of kiwis",
    "Gabriel has 67 of strawberries",
    "Ava has 95 of bananas",
    "Julian has 62 of mangoes",
    "Hannah has 0 of pineapples",
    "Lucas has 51 of watermelons",
    "Madeline has 18 of pears",
    "Oliver has 74 of apples",
    "Charlotte has 58 of grapes",
    "Thomas has 39 of kiwis",
    "Isabella has 22 of oranges",
    "Benjamin has 85 of mangoes",
    "Julia has 44 of strawberries",
    "William has 12 of bananas",
    "Elizabeth has 76 of pineapples",
    "Henry has 60 of watermelons"
]

docs = [Document(content=x) for i,x in enumerate(list_of_strings)]

auth_client_secret = AuthApiKey()
from dotenv import load_dotenv
env_vars = load_dotenv(".env") 

os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "2"

document_store = WeaviateDocumentStore(
    auth_client_secret=auth_client_secret,url=os.getenv("WEAVIATE_URL"))

TEMPLATE_QA="""
    Given these documents, write a information-dense and short answer regarding the question.\n
    Documents:
    {% for doc in documents %}
        {{ doc.content }}
    {% endfor %}

    \question: {{query}}
    \n Answer:
    """


@dataclass
class WrappedPipeline:
    pipeline: Pipeline
    run: object

OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://host.containers.internal:11434") 
MODEL_NAME = os.getenv("OLLAMA_MODEL", "llama3") 
def get_ollama_generator(modelname):
    generator = OllamaGenerator(model=modelname,
                            url=OLLAMA_URL, 
                            generation_kwargs={
                              "temperature": 0.3,
                              })
    return generator
def get_openai_generator(model_name):
    llm = OpenAIGenerator(model=model_name,generation_kwargs={"temperature":0.0})
    return llm

def get_simple_bm25_pipeline(document_store,prompt_template,generator=get_ollama_generator(MODEL_NAME)):
    retriever = WeaviateBM25Retriever(document_store=document_store)
    builder = PromptBuilder(template=prompt_template)
    p = Pipeline()
    p.add_component(instance=retriever,name="bm25_retriever")
    p.add_component(instance=builder, name="prompt_builder") 
    p.add_component(instance=generator, name="llm") 
    p.add_component(instance=AnswerBuilder(), name="answer_builder")
    
    p.connect("prompt_builder", "llm")
    p.connect("bm25_retriever", "prompt_builder.documents")
    p.connect("prompt_builder", "llm")
    p.connect("llm.replies", "answer_builder.replies")
    p.connect("llm.meta", "answer_builder.meta")
    p.connect("bm25_retriever", "answer_builder.documents")
    def run(query,top_k_bm25):
        return p.run(data={
            "bm25_retriever": {"query":query, "top_k": top_k_bm25},
            "prompt_builder": {"query": query},
            "answer_builder": {"query": query},
        })
    return WrappedPipeline(
        pipeline=p,
        run=run
    )
pipeline = get_simple_bm25_pipeline(document_store,TEMPLATE_QA)

# index function
def index_docs():
    document_store.write_documents(docs) 


app = FastAPI()
#FastAPIInstrumentor.instrument_app(app)
# get response function
@app.get("/ask_question")
def get_answer(query):
    return pipeline.run(query,3)["answer_builder"]["answers"][0].data


print("indexing documents")
index_docs()
print("gnerating answer")
print(get_answer("Who got pineapples? And how many?"))