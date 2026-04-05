from pydantic import BaseModel
from typing import Optional


class MensajeRequest(BaseModel):
    mensaje: str
    historial: list[dict] = []
    telefono: str = "local-test"


class MensajeResponse(BaseModel):
    respuesta: str
    reserva_creada: bool = False
    datos_reserva: Optional[dict] = None


class ReservaOut(BaseModel):
    id: int
    nombre: str
    telefono: str
    fecha: str
    hora: str
    cancha: int
    duracion: int
    confirmada: bool
    sni: str

    class Config:
        from_attributes = True


class DisponibilidadRequest(BaseModel):
    fecha: str
    hora: str
    duracion: int = 90