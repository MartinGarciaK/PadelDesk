# Padel Bot 

Asistente conversacional para reservas de canchas de pádel, desarrollado como proyecto personal. Permite a los usuarios reservar y cancelar turnos mediante lenguaje natural, con un panel de administración para gestionar el club.

## Demo

- **Chat con IA**: el usuario escribe en lenguaje natural y el bot extrae fecha, hora, nombre y DNI para crear la reserva.
- **Panel de admin**: vista de reservas, ocupación por cancha, bloqueos de horarios y creación manual de turnos.

## Stack

- **Backend**: Python, FastAPI, SQLAlchemy, SQLite
- **IA**: Groq API (Llama 3.3 70B)
- **Frontend**: HTML, CSS y JavaScript vanilla

## Instalación

### Requisitos
- Python 3.10+
- Cuenta en [Groq](https://groq.com) para obtener una API key gratuita

### Pasos

1. Cloná el repositorio:
```bash
git clone https://github.com/tu-usuario/padel-bot.git
cd padel-bot
```

2. Creá y activá el entorno virtual:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

3. Instalá las dependencias:
```bash
pip install -r requirements.txt
```

4. Creá el archivo `.env` en la raíz con tu API key de Groq:

5. Levantá el servidor:
```bash
uvicorn backend.main:app --reload
```

6. Abrí `frontend/index.html` en el navegador para usar el chat.
7. Abrí `frontend/admin.html` para acceder al panel de administración.
   - Usuario: `admin`
   - Contraseña: `admin123`

## Estructura
padel-bot/
├── backend/
│   ├── main.py          # FastAPI app y endpoints
│   ├── schemas.py       # Modelos Pydantic
│   ├── bot/
│   │   ├── agent.py     # Integración con Groq
│   │   └── prompts.py   # System prompt del bot
│   ├── db/
│   │   ├── models.py    # Modelos SQLAlchemy
│   │   └── crud.py      # Operaciones sobre la BD
│   └── services/
├── frontend/
│   ├── index.html       # Simulador de chat
│   └── admin.html       # Panel de administración
├── requirements.txt
└── .env                 # No se sube al repo

## Funcionalidades

- Reserva de canchas por chat en lenguaje natural
- Cancelación de turnos con validación por DNI
- Consulta de disponibilidad en tiempo real
- Panel de administración con login
- Vista de ocupación por cancha y horario
- Bloqueo manual de horarios
- Creación manual de reservas desde el panel