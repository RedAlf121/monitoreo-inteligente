from models.repositories.mongo_db_borrowing_repository import MongoDBBorrowingRepository

def scan_borrowings(collection_name: str = 'borrowings'):
    repository = MongoDBBorrowingRepository()
    borrowings = repository.list_all()
    for borrowing in borrowings:
        print(borrowing)

