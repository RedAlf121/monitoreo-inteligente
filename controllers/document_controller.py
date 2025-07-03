from fastapi import APIRouter, HTTPException, UploadFile, File
import os
from services.document_reader import load_document,process_rules
from fastapi.responses import FileResponse
from shutil import copyfile
import glob
router = APIRouter(prefix="/documents")

# Create a directory for cached documents
CACHE_DIR = "cached_documents"
os.makedirs(CACHE_DIR, exist_ok=True)
DOCUMENTS_SUBDIR = "documents"  # Subdirectorio para documentos
RULES_SUBDIR = "rules"
os.makedirs(os.path.join(CACHE_DIR, DOCUMENTS_SUBDIR), exist_ok=True)
os.makedirs(os.path.join(CACHE_DIR, RULES_SUBDIR), exist_ok=True)

@router.post("/upload/")
def upload_document(file: UploadFile = File(...)):
    file_path = os.path.join(CACHE_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    
    if file.size == 0:
        raise HTTPException(status_code=400, detail="No se ha subido ningún archivo")

    documents_dir = os.path.join(CACHE_DIR, DOCUMENTS_SUBDIR)
    existing_docs = glob.glob(os.path.join(documents_dir, "*"))
    for doc in existing_docs:
        os.remove(doc) 

    copyfile(file_path, os.path.join(documents_dir, file.filename))
    try:
        result = load_document(file_path)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    rules = process_rules(result)
    print(rules)
    rules_path = os.path.join(CACHE_DIR, RULES_SUBDIR, "rules.txt")
    with open(rules_path, "w", encoding="utf-8") as new_file:
        new_file.write(rules)
    

    for item in os.listdir(CACHE_DIR):
        item_path = os.path.join(CACHE_DIR, item)
        if os.path.isfile(item_path):  # Solo eliminar archivos
            os.remove(item_path)

    return {"message": "Rules created successfully"}



@router.get('/download/')
def get_document():
    document_dir = os.path.join(CACHE_DIR, DOCUMENTS_SUBDIR)
    
    if not os.path.exists(document_dir):
        raise HTTPException(status_code=404, detail="Directorio de documentos no encontrado")
    
    files = os.listdir(document_dir)
    
    files = [f for f in files if os.path.isfile(os.path.join(document_dir, f))]
    
    if not files:
        raise HTTPException(status_code=404, detail="No se encontraron archivos en el directorio")
    
    file_name = files[0]
    file_path = os.path.join(document_dir, file_name)
    
    extension = file_name.split(".")[-1].lower() if "." in file_name else ""
    media_types = {
        "pdf": "application/pdf",
        "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "doc": "application/msword",
        "txt": "text/plain",
        "csv": "text/csv",
        "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "jpg": "image/jpeg",
        "png": "image/png",
        "zip": "application/zip"
    }
    
    media_type = media_types.get(extension, "application/octet-stream")
    headers = {"Content-Disposition": f"attachment; filename={file_name}"}
    return FileResponse(
        path=file_path,
        filename=file_name,  # Nombre con el que se descargará
        media_type=media_type,
        headers=headers
    )