from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from models import SessionLocal, engine, Base, Vuelo
from typing import List

app = FastAPI()

class VueloCreate(BaseModel):
    codigo: str
    tipo: str
    estado: str

class VueloResponse(BaseModel):
    id: int
    codigo: str
    tipo: str
    estado: str

    class Config:
        orm_mode = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/vuelos/", response_model=VueloResponse)
def crear_vuelo(vuelo: VueloCreate, db: Session = Depends(get_db)):
    db_vuelo = Vuelo(codigo=vuelo.codigo, tipo=vuelo.tipo, estado=vuelo.estado)
    db.add(db_vuelo)
    db.commit()
    db.refresh(db_vuelo)
    return db_vuelo

@app.get("/vuelos/{vuelo_id}", response_model=VueloResponse)
def obtener_vuelo(vuelo_id: int, db: Session = Depends(get_db)):
    db_vuelo = db.query(Vuelo).filter(Vuelo.id == vuelo_id).first()
    if db_vuelo is None:
        raise HTTPException(status_code=404, detail="Vuelo no encontrado")
    return db_vuelo

@app.put("/vuelos/{vuelo_id}", response_model=VueloResponse)
def actualizar_vuelo(vuelo_id: int, vuelo: VueloCreate, db: Session = Depends(get_db)):
    db_vuelo = db.query(Vuelo).filter(Vuelo.id == vuelo_id).first()
    if db_vuelo is None:
        raise HTTPException(status_code=404, detail="Vuelo no encontrado")
    db_vuelo.codigo = vuelo.codigo
    db_vuelo.tipo = vuelo.tipo
    db_vuelo.estado = vuelo.estado
    db.commit()
    db.refresh(db_vuelo)
    return db_vuelo


@app.delete("/vuelos/{vuelo_id}")
def eliminar_vuelo(vuelo_id: int, db: Session = Depends(get_db)):
    db_vuelo = db.query(Vuelo).filter(Vuelo.id == vuelo_id).first()
    if db_vuelo is None:
        raise HTTPException(status_code=404, detail="Vuelo no encontrado")
    db.delete(db_vuelo)
    db.commit()
    return {"detail": "Vuelo eliminado"}


@app.patch("/vuelos/reordenar")
def reordenar_vuelos(vuelos_ids: list[int], db: Session = Depends(get_db)):
    
    vuelos = db.query(Vuelo).filter(Vuelo.id.in_(vuelos_ids)).all()
    if not vuelos:
        raise HTTPException(status_code=404, detail="Vuelos no encontrados")
    
    return {"detail": "Vuelos reordenados"}

@app.get("/vuelos/", response_model=List[VueloResponse])
def obtener_todos_los_vuelos(db: Session = Depends(get_db)):
    vuelos = db.query(Vuelo).all()  
    return vuelos

