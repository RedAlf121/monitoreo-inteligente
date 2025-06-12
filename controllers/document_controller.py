from fastapi import APIRouter, UploadFile, File
import os
from services.document_reader import load_document

router = APIRouter()

# Create a directory for cached documents
CACHE_DIR = "cached_documents"
os.makedirs(CACHE_DIR, exist_ok=True)

@router.post("/upload-document/")
def upload_document(file: UploadFile = File(...)):
    # Save the uploaded file to the cache directory
    file_path = os.path.join(CACHE_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    # Call the document reader service
    result = load_document(file_path)

    return {"message": result}