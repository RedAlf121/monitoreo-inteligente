from pymongo import MongoClient
import os 
from langchain.tools import tool


client = MongoClient(os.getenv("DB_ROUTE"))
db = client[os.getenv("DB_NAME")]

@tool
def list_databases() -> list:
    """List all databases available on the MongoDB server."""
    return client.list_database_names()

@tool
def list_collections() -> list:
    """List all collections in the initialized database."""
    return db.list_collection_names()

@tool
def find(collection_name: str, filter: dict = None, limit: int = 100) -> list:
    """Find documents in a collection using an optional filter. Limits to 100 results by default."""
    if filter is None:
        filter = {}
    results = list(db[collection_name].find(filter).limit(limit))
    for doc in results:
        doc.pop('_id', None)  # Remove ObjectId for easier serialization
    return results

@tool
def aggregate(collection_name: str, pipeline: list, limit: int = 100) -> list:
    """Run an aggregate query on a collection. Limits to 100 results by default."""
    results = list(db[collection_name].aggregate(pipeline))
    for doc in results:
        doc.pop('_id', None)
    return results[:limit]

def get_tools():
    """Return a list of all available MongoDB tools."""
    return [list_databases, list_collections, find, aggregate]

__all__ = ["get_tools"]



