from modelos.database import engine, Base
from modelos.producto import Categoria, Producto
from modelos.venta import Venta, DetalleVenta
from modelos.usuario import Usuario  # agregar esta línea

Base.metadata.create_all(engine)
print("Base de datos creada correctamente ✅")