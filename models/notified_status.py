from pydantic import BaseModel, Field
from typing import List

class NotifiedStatus(BaseModel):
    notified: List[str] = Field(default_factory=list, description="Lista de emails notificados")
    not_notified: List[str] = Field(default_factory=list, description="Lista de emails no notificados")

    def add_notified(self, email: str):
        if email not in self.notified:
            self.notified.append(email)

    def add_not_notified(self, email: str):
        if email not in self.not_notified:
            self.not_notified.append(email)

    def to_dict(self):
        return {"notified": self.notified, "not_notified": self.not_notified}
