from pydantic import BaseModel, EmailStr
from typing import Optional

class EtudiantBase(BaseModel):
    nom: str
    prenom: str
    email: EmailStr
    telephone: Optional[str] = None

class EtudiantCreate(EtudiantBase):
    pass

class Etudiant(EtudiantBase):
    id: int
    date_inscription: str  # format ISO (ex: "2025-01-29")

    class Config:
        from_attributes = True  # pour SQLAlchemy → Pydantic