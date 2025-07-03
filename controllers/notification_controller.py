from fastapi import APIRouter
import os
from fastapi.responses import JSONResponse, FileResponse
import json
import openpyxl

router = APIRouter(prefix="/documents")

@router.get("/notified-status")
def get_notified_status():
    file_path = "notified_status.json"
    if not os.path.exists(file_path):
        return JSONResponse(content={"error": "notified_status.json not found"}, status_code=404)
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

@router.get("/notified-status-excel")
def get_notified_status_excel():
    data = get_notified_status()
    # Si es un JSONResponse (error), retornarlo directamente
    if isinstance(data, JSONResponse):
        return data
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Notified Status"
    ws.append(["Status", "Email"])
    for email in data.get("notified", []):
        ws.append(["notified", email])
    for email in data.get("not_notified", []):
        ws.append(["not_notified", email])
    excel_path = os.path.join(os.path.dirname(__file__), "notified_status.xlsx")
    wb.save(excel_path)
    return FileResponse(excel_path, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename="notified_status.xlsx")

