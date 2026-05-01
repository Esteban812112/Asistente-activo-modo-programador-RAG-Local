import os
import json
from datetime import datetime

HISTORIAL_FILE = "historial.json"

def cargar_historial():
    if not os.path.exists(HISTORIAL_FILE):
        return []

    try:
        with open(HISTORIAL_FILE, "r", encoding="utf-8") as f:
            contenido = f.read().strip()

            if not contenido:
                return []

            return json.loads(contenido)

    except json.JSONDecodeError:
        return []

def guardar_historial(historial):
    with open(HISTORIAL_FILE, "w", encoding="utf-8") as f:
        json.dump(historial, f, indent=4, ensure_ascii=False)

def agregar_interaccion(usuario, respuesta):
    historial = cargar_historial()
    historial.append({
        "usuario": usuario,
        "respuesta": respuesta,
        "timestamp": datetime.now().strftime('%H:%M:%S')
    })
    guardar_historial(historial)