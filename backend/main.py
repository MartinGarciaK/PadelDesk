from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .schemas import MensajeRequest, MensajeResponse, ReservaOut, DisponibilidadRequest
from .db.models import init_db, get_db
from .db.crud import (
    crear_reserva, get_todas_las_reservas,
    get_canchas_disponibles, cancelar_reserva
)
from .bot.agent import chat_con_bot, verificar_ollama

app = FastAPI(title="Padel Bot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    init_db()


@app.get("/")
async def root():
    ollama_ok = await verificar_ollama()
    return {
        "status": "ok",
        "ollama": "conectado" if ollama_ok else "desconectado"
    }


@app.post("/chat", response_model=MensajeResponse)
async def chat(req: MensajeRequest, db: Session = Depends(get_db)):
    historial = req.historial + [{"role": "user", "content": req.mensaje}]

    # Extraer fecha y hora mencionadas para consultar disponibilidad real
    from datetime import datetime, timedelta
    hoy = datetime.now().strftime("%Y-%m-%d")
    manana = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    # Inyectar contexto de disponibilidad si el mensaje menciona una fecha/hora
    mensaje_lower = req.mensaje.lower()
    contexto_disponibilidad = ""

    fechas_a_chequear = []
    if "hoy" in mensaje_lower:
        fechas_a_chequear.append(hoy)
    if "mañana" in mensaje_lower or "manana" in mensaje_lower:
        fechas_a_chequear.append(manana)

    horas_comunes = ["08:00","09:00","10:00","11:00","12:00","13:00","14:00",
                     "15:00","16:00","17:00","18:00","19:00","20:00","21:00","22:00"]

    if fechas_a_chequear:
        lineas = []
        for fecha in fechas_a_chequear:
            disponibles = []
            ocupadas = []
            for hora in horas_comunes:
                canchas = get_canchas_disponibles(db, fecha, hora)
                if canchas:
                    disponibles.append(hora)
                else:
                    ocupadas.append(hora)
            lineas.append(f"Fecha {fecha} — horarios ocupados: {', '.join(ocupadas) if ocupadas else 'ninguno'} — horarios libres: {', '.join(disponibles)}")
        contexto_disponibilidad = "\n\nDISPONIBILIDAD REAL EN BASE DE DATOS:\n" + "\n".join(lineas)

    # Agregar contexto al último mensaje del historial
    if contexto_disponibilidad:
        historial[-1]["content"] += contexto_disponibilidad

    respuesta, datos_reserva = await chat_con_bot(historial)
  
    reserva_creada = False
    if datos_reserva:
        canchas_libres = get_canchas_disponibles(
            db,
            datos_reserva["fecha"],
            datos_reserva["hora"],
            datos_reserva.get("duracion", 90)
        )
        if not canchas_libres:
            respuesta = "Lo siento, no hay canchas disponibles para ese horario. ¿Querés probar con otro?"
        else:
            crear_reserva(
                db,
                nombre=datos_reserva["nombre"],
                telefono=req.telefono,
                fecha=datos_reserva["fecha"],
                hora=datos_reserva["hora"],
                cancha=canchas_libres[0].id,
                duracion=datos_reserva.get("duracion", 90),
                dni=datos_reserva.get("dni", "")
            )
            reserva_creada = True

    return MensajeResponse(
        respuesta=respuesta,
        reserva_creada=reserva_creada,
        datos_reserva=datos_reserva if reserva_creada else None
    )

@app.get("/reservas", response_model=list[ReservaOut])
async def listar_reservas(db: Session = Depends(get_db)):
    return get_todas_las_reservas(db)


@app.post("/disponibilidad")
async def disponibilidad(req: DisponibilidadRequest, db: Session = Depends(get_db)):
    canchas = get_canchas_disponibles(db, req.fecha, req.hora, req.duracion)
    return {
        "fecha": req.fecha,
        "hora": req.hora,
        "canchas_disponibles": [{"id": c.id, "nombre": c.nombre} for c in canchas]
    }


@app.delete("/reservas/{reserva_id}")
async def eliminar_reserva(reserva_id: int, db: Session = Depends(get_db)):
    ok = cancelar_reserva(db, reserva_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return {"ok": True}