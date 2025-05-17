from typing import Optional
from models.repositories.repository import Repository
from models.borrowing import Borrowing
from bson import ObjectId
from pymongo import MongoClient
from env_utils import get_env_vars

class MongoDBBorrowingRepository(Repository):
    def __init__(self):
        client = MongoClient(get_env_vars()["DB_ROUTE"])
        db = client[get_env_vars()["DB_NAME"]]
        self.collection = db["borrowings"]

    
    def get_by_id(self, id: str) -> Optional[Borrowing]:
        doc = self.collection.find_one({"_id": ObjectId(id)})
        if doc:
            doc["_id"] = str(doc["_id"])
            doc["id_user"] = str(doc["id_user"])
            return Borrowing(**doc)
        return None

    def list_all(self)-> list[Borrowing]:
        documents = self.collection.find()
        result = []
        for document in documents:
            document["_id"] = str(document["_id"])
            document["id_user"] = str(document["id_user"])
            borrowing_model = Borrowing(**document)
            result.append(borrowing_model)
        return result
