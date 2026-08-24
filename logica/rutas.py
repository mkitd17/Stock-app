import sys
import os


def obtener_carpeta_base():
    """
    Devuelve la carpeta donde deben guardarse los datos (base de datos, backups, tickets, config).
    - Si la app corre como .exe empaquetado: una carpeta en ProgramData (con permisos de escritura para cualquier usuario).
    - Si corre como script normal (python main.py): la raíz del proyecto.
    """
    if getattr(sys, "frozen", False):
        carpeta_datos = os.path.join(os.environ.get("PROGRAMDATA", "C:\\ProgramData"), "StockApp")
        os.makedirs(carpeta_datos, exist_ok=True)
        return carpeta_datos
    else:
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))