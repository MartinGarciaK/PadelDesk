from sqlalchemy.orm import Session
from .models import Reserva, Cancha
from datetime import datetime


def get_reservas_por_fecha(db: Session, fecha: str):
    return db.query(Reserva).filter(Reserva.fecha == fecha).all()


def get_reservas_por_fecha_y_cancha(db: Session, fecha: str, cancha: int):
    return db.query(Reserva).filter(
        Reserva.fecha == fecha,
        Reserva.cancha == cancha
    ).all()


def cancha_disponible(db: Session, fecha: str, hora: str, cancha: int, duracion: int = 90):
    reservas = get_reservas_por_fecha_y_cancha(db, fecha, cancha)
    hora_inicio_nueva = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")
    hora_fin_nueva = hora_inicio_nueva.replace(
        minute=hora_inicio_nueva.minute + duracion % 60,
        hour=hora_inicio_nueva.hour + duracion // 60
    )

    for r in reservas:
        hora_inicio_existente = datetime.strptime(f"{r.fecha} {r.hora}", "%Y-%m-%d %H:%M")
        hora_fin_existente = hora_inicio_existente.replace(
            minute=hora_inicio_existente.minute + r.duracion % 60,
            hour=hora_inicio_existente.hour + r.duracion // 60
        )
        if hora_inicio_nueva < hora_fin_existente and hora_fin_nueva > hora_inicio_existente:
            return False
    return True


def get_canchas_disponibles(db: Session, fecha: str, hora: str, duracion: int = 90):
    canchas = db.query(Cancha).filter(Cancha.activa == True).all()
    return [c for c in canchas if cancha_disponible(db, fecha, hora, c.id, duracion)]


def crear_reserva(db: Session, nombre: str, telefono: str, fecha: str,
                  hora: str, cancha: int, duracion: int = 90, dni: str = ""):
    reserva = Reserva(
        nombre=nombre,
        telefono=telefono,
        fecha=fecha,
        hora=hora,
        cancha=cancha,
        duracion=duracion,
        dni=dni,
        confirmada=True
    )
    db.add(reserva)
    db.commit()
    db.refresh(reserva)
    return reserva


def get_todas_las_reservas(db: Session):
    return db.query(Reserva).order_by(Reserva.fecha, Reserva.hora).all()

def buscar_reserva(db: Session, nombre: str, fecha: str, hora: str, dni: str):
    return db.query(Reserva).filter(
        Reserva.nombre.ilike(f"%{nombre}%"),
        Reserva.fecha == fecha,
        Reserva.hora == hora,
        Reserva.dni == dni
    ).first()

def cancelar_reserva(db: Session, reserva_id: int):
    reserva = db.query(Reserva).filter(Reserva.id == reserva_id).first()
    if reserva:
        db.delete(reserva)
        db.commit()
        return True
    return False