from pydantic import BaseModel, Field
from models.book import Book


class User(BaseModel):
    name: str = Field(description="User's full name")  
    email: str = Field(description="User's email address")  
    books: list[Book] = Field(description="List of borrowed books that the user has requested and must return")  

class Users(BaseModel):
    userList: list[User] = Field(description="list of users")