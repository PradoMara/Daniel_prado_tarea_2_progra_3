from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Vuelo(Base):
    __tablename__ = 'vuelos'

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, index=True)
    tipo = Column(String)  
    estado = Column(String)  


DATABASE_URL = "sqlite:///./vuelos.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)
