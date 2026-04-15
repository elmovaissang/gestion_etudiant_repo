from sqlalchemy.orm import Session
from . import models, schemas

def get_etudiant(db: Session, etudiant_id: int):
    return db.query(models.Etudiant).filter(models.Etudiant.id == etudiant_id).first()

def get_etudiants(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Etudiant).offset(skip).limit(limit).all()

def create_etudiant(db: Session, etudiant: schemas.EtudiantCreate):
    db_etudiant = models.Etudiant(**etudiant.model_dump())
    db.add(db_etudiant)
    db.commit()
    db.refresh(db_etudiant)
    return db_etudiant

def update_etudiant(db: Session, etudiant_id: int, etudiant: schemas.EtudiantCreate):
    db_etudiant = get_etudiant(db, etudiant_id)
    if not db_etudiant:
        return None
    for key, value in etudiant.model_dump().items():
        setattr(db_etudiant, key, value)
    db.commit()
    return db_etudiant

def delete_etudiant(db: Session, etudiant_id: int):
    db_etudiant = get_etudiant(db, etudiant_id)
    if db_etudiant:
        db.delete(db_etudiant)
        db.commit()
        return True
    return False