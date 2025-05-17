from abc import ABC, abstractmethod
from typing import Collection, Optional

from pydantic import BaseModel

from models.borrowing import Borrowing


class Repository(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_by_id(self, id: str) -> Optional[BaseModel]: ...

    @abstractmethod
    def list_all(self): ...

    
    