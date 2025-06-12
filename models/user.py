from pydantic import BaseModel, Field

class User(BaseModel):
    name: str = Field(description="User's full name")  
    email: str = Field(description="User's email address")  
    books: list = Field(description="List of borrowed books that the user has requested and must return")  
    category: str = Field(description="User's category based on their customer type")  


class Users(BaseModel):
    userList: list[User] = Field(description="list of users")