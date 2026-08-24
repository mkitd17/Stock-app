import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from logica.rutas import obtener_carpeta_base

# La base de datos se guarda en la carpeta que corresponda según el contexto
# (ProgramData si es .exe, la raíz del proyecto si es script)
RUTA_DB = os.path.join(obtener_carpeta_base(), "stock.db")

engine = create_engine(f"sqlite:///{RUTA_DB}", echo=False)

# Base de la que van a heredar todos nuestros modelos (tablas)
Base = declarative_base()

# Session: es lo que usamos para consultar/guardar datos
SessionLocal = sessionmaker(bind=engine)
