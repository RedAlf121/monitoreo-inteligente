from pydantic import BaseModel, Field

class Book(BaseModel):
    title: str = Field(description="The title of the book")
    code: str = Field(description="Many books have the same name, but not the same barcode")
    due_date: str = Field(description="The end date of the borrow")
