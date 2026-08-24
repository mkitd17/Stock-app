from sqlalchemy import func
from sqlalchemy.orm import joinedload
from modelos.database import SessionLocal
from modelos.producto import Producto, Categoria



def listar_productos(busqueda: str = ""):
    """Devuelve productos, filtrados por nombre o código de barras (sin importar mayúsc/minúsc)."""
    db = SessionLocal()
    query = db.query(Producto).options(joinedload(Producto.categoria))

    if busqueda:
        texto = f"%{busqueda.lower()}%"
        query = query.filter(
            func.lower(Producto.nombre).like(texto) |
            func.lower(Producto.codigo_barras).like(texto)
        )

    productos = query.order_by(Producto.nombre).all()
    db.close()
    return productos


def obtener_categorias():
    db = SessionLocal()
    categorias = db.query(Categoria).order_by(Categoria.nombre).all()
    db.close()
    return categorias


def agregar_producto(nombre, codigo_barras, categoria_id, precio_costo, precio_venta, stock_actual, stock_minimo):
    db = SessionLocal()
    producto = Producto(
        nombre=nombre,
        codigo_barras=codigo_barras or None,
        categoria_id=categoria_id,
        precio_costo=precio_costo,
        precio_venta=precio_venta,
        stock_actual=stock_actual,
        stock_minimo=stock_minimo,
    )
    db.add(producto)
    db.commit()
    db.close()


def actualizar_producto(producto_id, nombre, codigo_barras, categoria_id, precio_costo, precio_venta, stock_actual, stock_minimo):
    db = SessionLocal()
    producto = db.query(Producto).get(producto_id)
    if producto:
        producto.nombre = nombre
        producto.codigo_barras = codigo_barras or None
        producto.categoria_id = categoria_id
        producto.precio_costo = precio_costo
        producto.precio_venta = precio_venta
        producto.stock_actual = stock_actual
        producto.stock_minimo = stock_minimo
        db.commit()
    db.close()


def eliminar_producto(producto_id):
    db = SessionLocal()
    producto = db.query(Producto).get(producto_id)
    if producto:
        db.delete(producto)
        db.commit()
    db.close()

def crear_categoria(nombre: str):
    db = SessionLocal()
    categoria = Categoria(nombre=nombre.strip())
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    db.close()
    return categoria

def buscar_por_codigo_exacto(codigo: str):
    db = SessionLocal()
    producto = db.query(Producto).filter(Producto.codigo_barras == codigo.strip()).first()
    db.close()
    return producto