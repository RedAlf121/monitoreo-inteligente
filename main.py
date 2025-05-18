from fastapi import FastAPI
from controllers.document_controller import router as document_router

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}

app.include_router(document_router)