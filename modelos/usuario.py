from sqlalchemy import Column, Integer, String, Boolean
from modelos.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)
    nombre_usuario = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    salt = Column(String, nullable=False)
    rol = Column(String, nullable=False, default="vendedor")  # "admin" o "vendedor"
    activo = Column(Boolean, default=True)

    def __repr__(self):
        return f"<Usuario {self.nombre_usuario} ({self.rol})>"