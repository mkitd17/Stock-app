from sqlalchemy import func
from sqlalchemy.orm import joinedload
from modelos.database import SessionLocal
from modelos.producto import Producto
from modelos.venta import Venta, DetalleVenta


def buscar_producto_por_texto(texto: str):
    """Busca productos por nombre o código de barras exacto/parcial, para el vendedor."""
    db = SessionLocal()
    patron = f"%{texto.lower()}%"
    productos = (
        db.query(Producto)
        .filter(
            func.lower(Producto.nombre).like(patron) |
            func.lower(Producto.codigo_barras).like(patron)
        )
        .order_by(Producto.nombre)
        .limit(15)
        .all()
    )
    db.close()
    return productos


def confirmar_venta(items: list[dict], usuario_id: int = None):
    """
    items: lista de dicts con {"producto_id": int, "cantidad": int, "precio_unitario": float}
    Descuenta stock y guarda la venta. Devuelve la venta creada (con id y total).
    """
    db = SessionLocal()
    try:
        venta = Venta(total=0.0, usuario_id=usuario_id)
        db.add(venta)
        db.flush()  # para que la venta tenga un id antes de guardar los detalles

        total = 0.0
        for item in items:
            producto = db.query(Producto).get(item["producto_id"])
            if producto is None:
                raise ValueError(f"Producto {item['producto_id']} no encontrado")
            if producto.stock_actual < item["cantidad"]:
                raise ValueError(f"Stock insuficiente para '{producto.nombre}'")

            producto.stock_actual -= item["cantidad"]

            detalle = DetalleVenta(
                venta_id=venta.id,
                producto_id=producto.id,
                cantidad=item["cantidad"],
                precio_unitario=item["precio_unitario"],
            )
            db.add(detalle)
            total += item["cantidad"] * item["precio_unitario"]

        venta.total = total
        db.commit()
        db.refresh(venta)

        # Recargamos la venta con la relación "usuario" ya cargada,
        # para que se pueda leer después de cerrar la sesión sin errores
        venta_completa = (
            db.query(Venta)
            .options(joinedload(Venta.usuario))
            .filter(Venta.id == venta.id)
            .first()
        )
        return venta_completa
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def anular_venta(venta_id: int):
    """Marca la venta como anulada y devuelve el stock de cada producto vendido."""
    db = SessionLocal()
    try:
        venta = db.query(Venta).get(venta_id)
        if venta is None:
            raise ValueError("Venta no encontrada.")
        if venta.anulada:
            raise ValueError("Esta venta ya estaba anulada.")

        detalles = db.query(DetalleVenta).filter(DetalleVenta.venta_id == venta_id).all()
        for detalle in detalles:
            producto = db.query(Producto).get(detalle.producto_id)
            if producto:
                producto.stock_actual += detalle.cantidad

        venta.anulada = True
        db.commit()
        return venta
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def listar_ventas_recientes(limite: int = 50):
    """Últimas ventas, con nombre de usuario y estado, para poder anular alguna."""
    db = SessionLocal()
    ventas = (
        db.query(Venta)
        .options(joinedload(Venta.usuario))
        .order_by(Venta.id.desc())
        .limit(limite)
        .all()
    )
    db.close()
    return ventas