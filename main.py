from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine
from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Gestion Étudiants",
    description="CRUD complet pour la gestion des étudiants",
    version="1.0.0"
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/etudiants/", response_model=List[schemas.Etudiant])
def lire_etudiants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    etudiants = crud.get_etudiants(db, skip=skip, limit=limit)
    return etudiants

@app.get("/etudiants/{etudiant_id}", response_model=schemas.Etudiant)
def lire_etudiant(etudiant_id: int, db: Session = Depends(get_db)):
    db_etudiant = crud.get_etudiant(db, etudiant_id)
    if db_etudiant is None:
        raise HTTPException(status_code=404, detail="Étudiant non trouvé")
    return db_etudiant

@app.post("/etudiants/", response_model=schemas.Etudiant, status_code=201)
def creer_etudiant(etudiant: schemas.EtudiantCreate, db: Session = Depends(get_db)):
    db_etudiant = crud.create_etudiant(db=db, etudiant=etudiant)
    return db_etudiant

@app.put("/etudiants/{etudiant_id}", response_model=schemas.Etudiant)
def mettre_a_jour_etudiant(etudiant_id: int, etudiant: schemas.EtudiantCreate, db: Session = Depends(get_db)):
    db_etudiant = crud.update_etudiant(db, etudiant_id, etudiant)
    if db_etudiant is None:
        raise HTTPException(status_code=404, detail="Étudiant non trouvé")
    return db_etudiant

@app.delete("/etudiants/{etudiant_id}", response_model=dict)
def supprimer_etudiant(etudiant_id: int, db: Session = Depends(get_db)):
    success = crud.delete_etudiant(db, etudiant_id)
    if not success:
        raise HTTPException(status_code=404, detail="Étudiant non trouvé")
    return {"message": "Étudiant supprimé"}