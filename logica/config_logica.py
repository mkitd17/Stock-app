import json
import os
from logica.rutas import obtener_carpeta_base

RUTA_CONFIG = os.path.join(obtener_carpeta_base(), "configuracion.json")

VALORES_POR_DEFECTO = {"nombre_local": "Mi Negocio", "ruta_logo": ""}


def obtener_configuracion():
    if not os.path.exists(RUTA_CONFIG):
        return VALORES_POR_DEFECTO.copy()
    with open(RUTA_CONFIG, "r", encoding="utf-8") as f:
        datos = json.load(f)
    return {**VALORES_POR_DEFECTO, **datos}


def guardar_configuracion(nombre_local, ruta_logo):
    datos = {"nombre_local": nombre_local, "ruta_logo": ruta_logo}
    with open(RUTA_CONFIG, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)