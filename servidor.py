from flask import Flask, jsonify, request
from modelos.producto import Categoria, Producto
from modelos.venta import Venta, DetalleVenta
from modelos.usuario import Usuario
from logica.productos_logica import (
    listar_productos, agregar_producto, actualizar_producto,
    eliminar_producto, obtener_categorias, crear_categoria
)
from logica.ventas_logica import confirmar_venta, listar_ventas_recientes, anular_venta
from logica.ticket_logica import generar_ticket_pdf
app = Flask(__name__)


def producto_a_dict(p):
    return {
        "id": p.id,
        "nombre": p.nombre,
        "codigo_barras": p.codigo_barras,
        "precio_costo": p.precio_costo,
        "precio_venta": p.precio_venta,
        "stock_actual": p.stock_actual,
        "stock_minimo": p.stock_minimo,
        "categoria_id": p.categoria_id,
        "categoria": p.categoria.nombre if p.categoria else None,
    }


@app.route("/productos", methods=["GET"])
def obtener_productos():
    busqueda = request.args.get("busqueda", "")
    productos = listar_productos(busqueda)
    return jsonify([producto_a_dict(p) for p in productos])


@app.route("/productos", methods=["POST"])
def crear_producto():
    datos = request.get_json()
    try:
        agregar_producto(
            nombre=datos["nombre"],
            codigo_barras=datos.get("codigo_barras"),
            categoria_id=datos.get("categoria_id"),
            precio_costo=datos.get("precio_costo", 0),
            precio_venta=datos.get("precio_venta", 0),
            stock_actual=datos.get("stock_actual", 0),
            stock_minimo=datos.get("stock_minimo", 0),
        )
        return jsonify({"mensaje": "Producto creado correctamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/productos/<int:producto_id>", methods=["PUT"])
def editar_producto(producto_id):
    datos = request.get_json()
    try:
        actualizar_producto(
            producto_id,
            nombre=datos["nombre"],
            codigo_barras=datos.get("codigo_barras"),
            categoria_id=datos.get("categoria_id"),
            precio_costo=datos.get("precio_costo", 0),
            precio_venta=datos.get("precio_venta", 0),
            stock_actual=datos.get("stock_actual", 0),
            stock_minimo=datos.get("stock_minimo", 0),
        )
        return jsonify({"mensaje": "Producto actualizado correctamente"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/productos/<int:producto_id>", methods=["DELETE"])
def borrar_producto(producto_id):
    try:
        eliminar_producto(producto_id)
        return jsonify({"mensaje": "Producto eliminado correctamente"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/categorias", methods=["GET"])
def obtener_categorias_endpoint():
    categorias = obtener_categorias()
    return jsonify([{"id": c.id, "nombre": c.nombre} for c in categorias])


@app.route("/categorias", methods=["POST"])
def crear_categoria_endpoint():
    datos = request.get_json()
    try:
        categoria = crear_categoria(datos["nombre"])
        return jsonify({"id": categoria.id, "nombre": categoria.nombre}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


def venta_a_dict(v):
    return {
        "id": v.id,
        "fecha": v.fecha.strftime("%d/%m/%Y %H:%M"),
        "total": v.total,
        "anulada": v.anulada,
        "usuario": v.usuario.nombre_usuario if v.usuario else None,
    }


@app.route("/ventas", methods=["GET"])
def obtener_ventas():
    ventas = listar_ventas_recientes()
    return jsonify([venta_a_dict(v) for v in ventas])


@app.route("/ventas", methods=["POST"])
def crear_venta():
    datos = request.get_json()
    items = datos.get("items", [])
    usuario_id = datos.get("usuario_id")

    if not items:
        return jsonify({"error": "El carrito está vacío"}), 400

    try:
        venta = confirmar_venta(items, usuario_id=usuario_id)
        return jsonify(venta_a_dict(venta)), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.route("/ventas/<int:venta_id>/anular", methods=["POST"])
def anular_venta_endpoint(venta_id):
    try:
        venta = anular_venta(venta_id)
        return jsonify({"mensaje": "Venta anulada correctamente", "venta": venta_a_dict(venta)})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.route("/ventas/<int:venta_id>/ticket", methods=["POST"])
def generar_ticket_endpoint(venta_id):
    from modelos.database import SessionLocal
    from modelos.venta import Venta, DetalleVenta
    from sqlalchemy.orm import joinedload

    datos = request.get_json()
    formato = datos.get("formato", "ticket")

    db = SessionLocal()
    venta = db.query(Venta).get(venta_id)
    if venta is None:
        db.close()
        return jsonify({"error": "Venta no encontrada"}), 404

    detalles = (
        db.query(DetalleVenta)
        .options(joinedload(DetalleVenta.producto))
        .filter(DetalleVenta.venta_id == venta_id)
        .all()
    )

    items_ticket = [
        {
            "nombre": d.producto.nombre,
            "cantidad": d.cantidad,
            "precio_unitario": d.precio_unitario,
            "subtotal": d.subtotal,
        }
        for d in detalles
    ]
    db.close()

    ruta_pdf = generar_ticket_pdf(venta, items_ticket, formato=formato)
    return jsonify({"ruta": ruta_pdf})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)