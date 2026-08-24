from datetime import datetime, timedelta
from sqlalchemy import func
from modelos.database import SessionLocal
from modelos.producto import Producto
from modelos.venta import Venta, DetalleVenta


def resumen_periodo(desde: datetime, hasta: datetime):
    """Total facturado y cantidad de ventas entre dos fechas (inclusive), sin contar anuladas."""
    db = SessionLocal()
    resultado = (
        db.query(func.count(Venta.id), func.coalesce(func.sum(Venta.total), 0.0))
        .filter(Venta.fecha >= desde, Venta.fecha <= hasta, Venta.anulada == False)
        .first()
    )
    db.close()
    cantidad_ventas, total = resultado
    return {"cantidad_ventas": cantidad_ventas, "total": total}


def productos_mas_vendidos(desde: datetime, hasta: datetime, limite: int = 10):
    """Ranking de productos por cantidad vendida en el período."""
    db = SessionLocal()
    resultados = (
        db.query(
            Producto.nombre,
            func.sum(DetalleVenta.cantidad).label("total_unidades"),
            func.sum(DetalleVenta.cantidad * DetalleVenta.precio_unitario).label("total_facturado"),
        )
        .join(DetalleVenta, DetalleVenta.producto_id == Producto.id)
        .join(Venta, Venta.id == DetalleVenta.venta_id)
        .filter(Venta.fecha >= desde, Venta.fecha <= hasta, Venta.anulada == False)
        .group_by(Producto.id)
        .order_by(func.sum(DetalleVenta.cantidad).desc())
        .limit(limite)
        .all()
    )
    db.close()
    return resultados


def productos_stock_bajo():
    """Productos cuyo stock actual está en o por debajo del mínimo definido."""
    db = SessionLocal()
    productos = (
        db.query(Producto)
        .filter(Producto.stock_actual <= Producto.stock_minimo)
        .order_by(Producto.stock_actual)
        .all()
    )
    db.close()
    return productos


def rango_hoy():
    hoy = datetime.now().date()
    desde = datetime.combine(hoy, datetime.min.time())
    hasta = datetime.combine(hoy, datetime.max.time())
    return desde, hasta


def rango_ultimos_dias(dias: int):
    hasta = datetime.now()
    desde = hasta - timedelta(days=dias)
    return desde, hasta