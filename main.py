from fastapi import FastAPI
import os
from astrapy import DataAPIClient  # ✅ Use astrapy instead of AstraDocumentStore

app = FastAPI()

# Retrieve AstraDB credentials from Kubernetes Secrets
astra_endpoint = os.getenv("ASTRA_DB_API_ENDPOINT")
astra_token = os.getenv("ASTRA_DB_APPLICATION_TOKEN")

# Debugging: Print the values
print(f"DEBUG: ASTRA_DB_API_ENDPOINT = {astra_endpoint}")
print(f"DEBUG: ASTRA_DB_APPLICATION_TOKEN = {astra_token}")

# ✅ Connect to AstraDB
client = DataAPIClient(astra_token)
db = client.get_database_by_api_endpoint(astra_endpoint)

@app.get("/")
def read_root():
    return {"message": "Haystack Pipeline läuft!"}

@app.get("/test_db")
def test_db():
    try:
        collections = db.list_collection_names()
        print(f"DEBUG: Available collections: {collections}")

        # Fetch all documents from the first collection (if exists)
        if collections:
            collection = db.get_collection("test_collection")
            docs = collection.find({})  # ✅ Use .find() instead of .find_many()
            docs_list = list(docs)  # Convert generator to list
            print(f"DEBUG: Documents in collection: {docs_list}")

            return {"status": "Connected", "collections": collections, "documents": docs_list}
        else:
            return {"status": "Connected", "collections": collections, "documents": "No documents found"}
    except Exception as e:
        return {"status": "Error", "message": str(e)}
