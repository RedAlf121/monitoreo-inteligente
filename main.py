from fastapi import FastAPI
from controllers.item_controller import router as item_router

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}

app.include_router(item_router)