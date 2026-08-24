import os
import shutil
from datetime import datetime
from logica.rutas import obtener_carpeta_base

CARPETA_BASE = obtener_carpeta_base()
CARPETA_BACKUPS = os.path.join(CARPETA_BASE, "backups")
RUTA_DB = os.path.join(CARPETA_BASE, "stock.db")

MAXIMO_BACKUPS = 30  # cuántos backups conservar como máximo


def crear_backup():
    """Copia la base de datos actual a la carpeta de backups, con fecha y hora en el nombre."""
    if not os.path.exists(RUTA_DB):
        return None

    os.makedirs(CARPETA_BACKUPS, exist_ok=True)

    marca_tiempo = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nombre_backup = f"stock_backup_{marca_tiempo}.db"
    ruta_backup = os.path.join(CARPETA_BACKUPS, nombre_backup)

    shutil.copy2(RUTA_DB, ruta_backup)
    _limpiar_backups_viejos()
    return ruta_backup


def listar_backups():
    """Devuelve los backups existentes, del más reciente al más viejo."""
    if not os.path.exists(CARPETA_BACKUPS):
        return []

    archivos = [
        f for f in os.listdir(CARPETA_BACKUPS)
        if f.startswith("stock_backup_") and f.endswith(".db")
    ]
    archivos.sort(reverse=True)  # el nombre incluye la fecha, así que ordena cronológicamente
    return archivos


def restaurar_backup(nombre_archivo):
    """Reemplaza la base de datos actual por un backup elegido. Devuelve True si salió bien."""
    ruta_backup = os.path.join(CARPETA_BACKUPS, nombre_archivo)
    if not os.path.exists(ruta_backup):
        return False

    # Por seguridad, hacemos un backup de la base actual ANTES de sobreescribirla
    crear_backup()

    shutil.copy2(ruta_backup, RUTA_DB)
    return True


def _limpiar_backups_viejos():
    """Si hay más backups que el máximo permitido, borra los más viejos."""
    archivos = listar_backups()
    if len(archivos) > MAXIMO_BACKUPS:
        for archivo in archivos[MAXIMO_BACKUPS:]:
            os.remove(os.path.join(CARPETA_BACKUPS, archivo))