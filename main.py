import asyncio
from fastapi import FastAPI
from controllers.document_controller import router as document_router
from env_utils import init_env_vars, get_env_vars
from services.scanner.borrow_scan import scan_borrowings,get_agent_response
from services.scheduler.watcher import start_watching
from dotenv import load_dotenv

if __name__ == '__main__':
    init_env_vars()
    load_dotenv()
    app = FastAPI()
    app.include_router(document_router)
    #start_watching()
    #use_scanner_agent()
    asyncio.run(get_agent_response())
    #asyncio.run(scan_borrowings())
    #scan_borrowings()


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}

app.include_router(document_router)
