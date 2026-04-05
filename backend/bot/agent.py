import json
import os
from groq import Groq
from dotenv import load_dotenv
from .prompts import get_system_prompt

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"


async def chat_con_bot(historial: list[dict]) -> tuple[str, dict | None, dict | None]:
    messages = [
        {"role": "system", "content": get_system_prompt()},
        *historial
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.3,
        max_tokens=500
    )

    texto = response.choices[0].message.content.strip()

    datos_reserva = None
    datos_cancelacion = None

    if "RESERVA_LISTA:" in texto:
        try:
            json_str = texto.split("RESERVA_LISTA:")[1].strip()
            datos_reserva = json.loads(json_str)
            texto = "Perfecto, tu reserva está confirmada. Te esperamos en el club."
        except (json.JSONDecodeError, IndexError):
            pass

    elif "CANCELAR_RESERVA:" in texto:
        try:
            json_str = texto.split("CANCELAR_RESERVA:")[1].strip()
            datos_cancelacion = json.loads(json_str)
            texto = "procesando_cancelacion"
        except (json.JSONDecodeError, IndexError):
            pass

    return texto, datos_reserva, datos_cancelacion


async def verificar_ollama() -> bool:
    try:
        return bool(client.api_key)
    except Exception:
        return False