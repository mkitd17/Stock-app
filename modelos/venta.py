from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from modelos.database import Base


class Venta(Base):
    __tablename__ = "ventas"

    id = Column(Integer, primary_key=True)
    fecha = Column(DateTime, default=datetime.now)
    total = Column(Float, default=0.0)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)  # nuevo
    anulada = Column(Boolean, default=False)

    detalles = relationship("DetalleVenta", back_populates="venta", cascade="all, delete-orphan")
    usuario = relationship("Usuario")  # nuevo

    def __repr__(self):
        return f"<Venta {self.id} - ${self.total:.2f}>"


class DetalleVenta(Base):
    __tablename__ = "detalle_ventas"

    id = Column(Integer, primary_key=True)
    venta_id = Column(Integer, ForeignKey("ventas.id"))
    producto_id = Column(Integer, ForeignKey("productos.id"))

    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)  # guardamos el precio al momento de la venta

    venta = relationship("Venta", back_populates="detalles")
    producto = relationship("Producto")

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario