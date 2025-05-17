from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Borrowing(BaseModel):
    _id: Optional[str]
    fecha_prestamo: datetime
    fecha_devolucion: datetime
    estado: str
    cod_ejemplar: str
    id_user: str
