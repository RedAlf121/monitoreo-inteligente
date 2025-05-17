from fastapi import FastAPI
from controllers.document_controller import router as document_router
from env_utils import init_env_vars, get_env_vars
from services.scanner.borrow_scan import scan_borrowings
from services.scheduler.watcher import start_watching

if __name__ == '__main__':
    init_env_vars()
    print(get_env_vars())
    app = FastAPI()
    app.include_router(document_router)
    start_watching()

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}

app.include_router(document_router)
