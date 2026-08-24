import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from logica.config_logica import obtener_configuracion
from logica.rutas import obtener_carpeta_base

# Carpeta del proyecto (independiente de desde dónde se ejecute la app)
CARPETA_BASE = obtener_carpeta_base()
CARPETA_TICKETS = os.path.join(CARPETA_BASE, "tickets")


def generar_ticket_pdf(venta, items, formato="ticket"):
    """
    formato: "ticket" (80mm, para impresora térmica) o "a4" (hoja completa)
    Devuelve la ruta absoluta del PDF generado.
    """
    os.makedirs(CARPETA_TICKETS, exist_ok=True)

    if formato == "a4":
        ruta = _generar_pdf_a4(venta, items)
    else:
        ruta = _generar_pdf_ticket(venta, items)

    if not os.path.exists(ruta):
        raise FileNotFoundError(f"No se pudo generar el PDF en {ruta}")

    return ruta


def _generar_pdf_ticket(venta, items):
    config = obtener_configuracion()
    ruta_salida = os.path.join(CARPETA_TICKETS, f"ticket_{venta.id}.pdf")

    ancho = 80 * mm
    alto_logo = 22 * mm if config["ruta_logo"] and os.path.exists(config["ruta_logo"]) else 0
    alto = (55 + len(items) * 8) * mm + alto_logo

    c = canvas.Canvas(ruta_salida, pagesize=(ancho, alto))
    y = alto - 8 * mm

    if alto_logo:
        c.drawImage(
            config["ruta_logo"],
            (ancho - 28 * mm) / 2, y - 20 * mm,
            width=28 * mm, height=20 * mm,
            preserveAspectRatio=True, mask="auto"
        )
        y -= 22 * mm

    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(ancho / 2, y, config["nombre_local"])
    y -= 6 * mm

    c.setFont("Helvetica", 8)
    c.drawCentredString(ancho / 2, y, f"Ticket #{venta.id}")
    y -= 4.5 * mm
    c.drawCentredString(ancho / 2, y, venta.fecha.strftime("%d/%m/%Y %H:%M"))
    y -= 5 * mm

    c.line(3 * mm, y, ancho - 3 * mm, y)
    y -= 5 * mm

    c.setFont("Helvetica", 7.5)
    for item in items:
        c.drawString(3 * mm, y, item["nombre"][:26])
        y -= 3.5 * mm
        detalle = f'{item["cantidad"]} x ${item["precio_unitario"]:.2f}'
        c.drawString(3 * mm, y, detalle)
        c.drawRightString(ancho - 3 * mm, y, f'${item["subtotal"]:.2f}')
        y -= 5.5 * mm

    c.line(3 * mm, y, ancho - 3 * mm, y)
    y -= 6 * mm

    c.setFont("Helvetica-Bold", 10)
    c.drawRightString(ancho - 3 * mm, y, f"TOTAL: ${venta.total:.2f}")
    y -= 8 * mm

    c.setFont("Helvetica", 7)
    c.drawCentredString(ancho / 2, y, "¡Gracias por su compra!")

    c.save()
    return ruta_salida


def _generar_pdf_a4(venta, items):
    config = obtener_configuracion()
    ruta_salida = os.path.join(CARPETA_TICKETS, f"factura_{venta.id}.pdf")

    ancho, alto = A4
    c = canvas.Canvas(ruta_salida, pagesize=A4)
    y = alto - 25 * mm

    if config["ruta_logo"] and os.path.exists(config["ruta_logo"]):
        c.drawImage(
            config["ruta_logo"], 25 * mm, y - 20 * mm,
            width=35 * mm, height=25 * mm,
            preserveAspectRatio=True, mask="auto"
        )
        c.setFont("Helvetica-Bold", 18)
        c.drawString(70 * mm, y - 5 * mm, config["nombre_local"])
        y -= 30 * mm
    else:
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(ancho / 2, y, config["nombre_local"])
        y -= 12 * mm

    c.setFont("Helvetica", 10)
    c.drawCentredString(ancho / 2, y, f"Comprobante de venta #{venta.id}")
    y -= 6 * mm
    c.drawCentredString(ancho / 2, y, venta.fecha.strftime("%d/%m/%Y %H:%M"))
    y -= 12 * mm

    c.line(25 * mm, y, ancho - 25 * mm, y)
    y -= 8 * mm

    c.setFont("Helvetica-Bold", 10)
    c.drawString(25 * mm, y, "Producto")
    c.drawString(125 * mm, y, "Cantidad")
    c.drawString(150 * mm, y, "P. Unitario")
    c.drawRightString(ancho - 25 * mm, y, "Subtotal")
    y -= 5 * mm
    c.line(25 * mm, y, ancho - 25 * mm, y)
    y -= 8 * mm

    c.setFont("Helvetica", 10)
    for item in items:
        c.drawString(25 * mm, y, item["nombre"][:40])
        c.drawString(125 * mm, y, str(item["cantidad"]))
        c.drawString(150 * mm, y, f'${item["precio_unitario"]:.2f}')
        c.drawRightString(ancho - 25 * mm, y, f'${item["subtotal"]:.2f}')
        y -= 8 * mm

        if y < 40 * mm:
            c.showPage()
            y = alto - 25 * mm
            c.setFont("Helvetica", 10)

    y -= 4 * mm
    c.line(25 * mm, y, ancho - 25 * mm, y)
    y -= 10 * mm

    c.setFont("Helvetica-Bold", 14)
    c.drawRightString(ancho - 25 * mm, y, f"TOTAL: ${venta.total:.2f}")
    y -= 15 * mm

    c.setFont("Helvetica", 9)
    c.drawCentredString(ancho / 2, y, "¡Gracias por su compra!")

    c.save()
    return ruta_salida