import os
from langchain_mongodb.agent_toolkit.toolkit import MongoDBDatabaseToolkit
from langchain_mongodb.agent_toolkit.database import MongoDBDatabase
from pymongo import MongoClient


class MongoToolkit:
    langchain_toolkit: MongoDBDatabaseToolkit
    client: MongoClient
    database: MongoDBDatabase

    def __init__(self, llm):
        self.client = MongoClient(host=os.getenv("DB_ROUTE"))
        self.database = MongoDBDatabase(client=self.client,database=os.getenv("DB_NAME"))
        self.langchain_toolkit = MongoDBDatabaseToolkit(db=self.database,llm=llm)
    
    def tools(self):
        return self.langchain_toolkit.get_tools()