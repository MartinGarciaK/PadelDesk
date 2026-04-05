from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///./padel.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Reserva(Base):
    __tablename__ = "reservas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    dni = Column(String, nullable=False)
    telefono = Column(String, nullable=False)
    fecha = Column(String, nullable=False)       # "2025-04-10"
    hora = Column(String, nullable=False)         # "20:00"
    cancha = Column(Integer, nullable=False)      # 1, 2, 3...
    duracion = Column(Integer, default=90)        # minutos
    confirmada = Column(Boolean, default=False)
    creada_en = Column(DateTime, default=datetime.now)


class Cancha(Base):
    __tablename__ = "canchas"

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)       # "Cancha 1"
    activa = Column(Boolean, default=True)


def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    if db.query(Cancha).count() == 0:
        canchas = [Cancha(id=i, nombre=f"Cancha {i}") for i in range(1, 5)]
        db.add_all(canchas)
        db.commit()
    db.close()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()