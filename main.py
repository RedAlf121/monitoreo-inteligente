import asyncio
from threading import Thread
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.document_controller import router as document_router
from controllers.notification_controller import router as notification_router
from env_utils import init_env_vars, get_env_vars
from services.scanner.borrow_scan import scan_borrowings,get_agent_response,scan_mock_borrowings
from services.scheduler.watcher import start_watching
from dotenv import load_dotenv
import uvicorn

 
init_env_vars()
load_dotenv()
app = FastAPI()
app.add_middleware(
#["*"] is temporal only for development
CORSMiddleware,
allow_origins=["*"], 
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)
app.include_router(document_router)
app.include_router(notification_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}


if __name__ == "__main__":
    thread = Thread(target=start_watching,daemon=True)
    thread.start()
    uvicorn.run("main:app",reload=True,headers=[("Access-Control-Allow-Origin", "*")])
    #For testing:
    #use_scanner_agent()
    #print(asyncio.run(get_agent_response()))
    #print(scan_mock_borrowings())
    #asyncio.run(scan_borrowings())
    #scan_borrowings()

