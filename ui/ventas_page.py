import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QLabel, QListWidget, QListWidgetItem,
    QMessageBox, QInputDialog, QHeaderView
)
from PySide6.QtCore import Qt
from logica.ventas_logica import buscar_producto_por_texto, confirmar_venta
from logica.productos_logica import buscar_por_codigo_exacto
from logica.ticket_logica import generar_ticket_pdf


class VentasPage(QWidget):
    def __init__(self, usuario_actual=None):
        super().__init__()
        self.usuario_actual = usuario_actual
        layout = QVBoxLayout(self)

        self.carrito = []  # lista de dicts: producto, cantidad

        # --- Buscador ---
        self.input_busqueda = QLineEdit()
        self.input_busqueda.setPlaceholderText("Buscar producto por nombre o código de barras...")
        self.input_busqueda.textChanged.connect(self.actualizar_resultados)
        layout.addWidget(self.input_busqueda)
       
        # --- Campo de escaneo rápido ---
        self.input_scanner = QLineEdit()
        self.input_scanner.setPlaceholderText("📷 Escanear código de barras aquí...")
        self.input_scanner.setStyleSheet("font-size: 16px; padding: 6px; border: 2px solid #4CAF50;")
        self.input_scanner.returnPressed.connect(self.procesar_escaneo)
        layout.addWidget(self.input_scanner)

        # --- Lista de resultados de búsqueda ---
        self.lista_resultados = QListWidget()
        self.lista_resultados.setMaximumHeight(120)
        self.lista_resultados.itemDoubleClicked.connect(self.agregar_al_carrito)
        layout.addWidget(self.lista_resultados)

        barra_agregar = QHBoxLayout()
        ayuda = QLabel("Seleccioná un producto de la lista")
        ayuda.setStyleSheet("color: gray; font-size: 11px;")
        self.btn_agregar_carrito = QPushButton("➕ Agregar al carrito")
        self.btn_agregar_carrito.clicked.connect(self.agregar_seleccionado)
        barra_agregar.addWidget(ayuda)
        barra_agregar.addStretch()
        barra_agregar.addWidget(self.btn_agregar_carrito)
        layout.addLayout(barra_agregar)

        # --- Tabla del carrito ---
        self.tabla_carrito = QTableWidget()
        self.tabla_carrito.setColumnCount(4)
        self.tabla_carrito.setHorizontalHeaderLabels(["Producto", "Cantidad", "Precio unit.", "Subtotal"])
        self.tabla_carrito.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tabla_carrito.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla_carrito.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.tabla_carrito)

        # --- Botones del carrito ---
        botones_carrito = QHBoxLayout()
        self.btn_quitar = QPushButton("Quitar seleccionado")
        self.btn_vaciar = QPushButton("Vaciar carrito")
        self.btn_quitar.clicked.connect(self.quitar_seleccionado)
        self.btn_vaciar.clicked.connect(self.vaciar_carrito)
        botones_carrito.addWidget(self.btn_quitar)
        botones_carrito.addWidget(self.btn_vaciar)
        layout.addLayout(botones_carrito)

        # --- Total y confirmar ---
        barra_total = QHBoxLayout()
        self.label_total = QLabel("Total: $0.00")
        self.label_total.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.btn_confirmar = QPushButton("✅ Confirmar venta")
        self.btn_confirmar.setMinimumHeight(40)
        self.btn_confirmar.clicked.connect(self.confirmar)
        barra_total.addWidget(self.label_total)
        barra_total.addStretch()
        barra_total.addWidget(self.btn_confirmar)
        layout.addLayout(barra_total)

        self.resultados_actuales = []
        self.input_scanner.setFocus()

    def actualizar_resultados(self):
        texto = self.input_busqueda.text().strip()
        self.lista_resultados.clear()
        self.resultados_actuales = []

        if not texto:
            return

        self.resultados_actuales = buscar_producto_por_texto(texto)
        for producto in self.resultados_actuales:
            item = QListWidgetItem(f"{producto.nombre} — ${producto.precio_venta:.2f} (stock: {producto.stock_actual})")
            self.lista_resultados.addItem(item)

    def agregar_al_carrito(self, item):
        fila = self.lista_resultados.row(item)
        self.agregar_producto_de_fila(fila)

    def agregar_seleccionado(self):
        fila = self.lista_resultados.currentRow()
        if fila < 0:
            QMessageBox.information(self, "Sin selección", "Seleccioná un producto de la lista primero.")
            return
        self.agregar_producto_de_fila(fila)

    def agregar_producto_de_fila(self, fila):
        producto = self.resultados_actuales[fila]

        if producto.stock_actual <= 0:
            QMessageBox.warning(self, "Sin stock", f"'{producto.nombre}' no tiene stock disponible.")
            return

        cantidad, ok = QInputDialog.getInt(self, "Cantidad", f"¿Cuántas unidades de '{producto.nombre}'?", 1, 1, producto.stock_actual)
        if not ok:
            return

        # Si ya está en el carrito, sumamos la cantidad
        for linea in self.carrito:
            if linea["producto"].id == producto.id:
                linea["cantidad"] += cantidad
                self.actualizar_tabla_carrito()
                return

        self.carrito.append({"producto": producto, "cantidad": cantidad})
        self.actualizar_tabla_carrito()

        self.input_busqueda.clear()
        self.lista_resultados.clear()
    def procesar_escaneo(self):
        codigo = self.input_scanner.text().strip()
        self.input_scanner.clear()

        if not codigo:
            return

        producto = buscar_por_codigo_exacto(codigo)
        if producto is None:
            QMessageBox.warning(self, "No encontrado", f"No hay ningún producto con el código '{codigo}'.")
            return

        if producto.stock_actual <= 0:
            QMessageBox.warning(self, "Sin stock", f"'{producto.nombre}' no tiene stock disponible.")
            return

        # Si ya está en el carrito, sumamos 1. Si no, lo agregamos con cantidad 1.
        for linea in self.carrito:
            if linea["producto"].id == producto.id:
                if linea["cantidad"] + 1 > producto.stock_actual:
                    QMessageBox.warning(self, "Stock insuficiente", f"No queda más stock de '{producto.nombre}'.")
                    return
                linea["cantidad"] += 1
                self.actualizar_tabla_carrito()
                self.input_scanner.setFocus()
                return

        self.carrito.append({"producto": producto, "cantidad": 1})
        self.actualizar_tabla_carrito()
        self.input_scanner.setFocus()

    def actualizar_tabla_carrito(self):
        self.tabla_carrito.setRowCount(len(self.carrito))
        total = 0.0

        for fila, linea in enumerate(self.carrito):
            producto = linea["producto"]
            cantidad = linea["cantidad"]
            subtotal = cantidad * producto.precio_venta
            total += subtotal

            self.tabla_carrito.setItem(fila, 0, QTableWidgetItem(producto.nombre))
            self.tabla_carrito.setItem(fila, 1, QTableWidgetItem(str(cantidad)))
            self.tabla_carrito.setItem(fila, 2, QTableWidgetItem(f"${producto.precio_venta:.2f}"))
            self.tabla_carrito.setItem(fila, 3, QTableWidgetItem(f"${subtotal:.2f}"))

        self.label_total.setText(f"Total: ${total:.2f}")

    def quitar_seleccionado(self):
        fila = self.tabla_carrito.currentRow()
        if fila < 0:
            return
        self.carrito.pop(fila)
        self.actualizar_tabla_carrito()

    def vaciar_carrito(self):
        self.carrito = []
        self.actualizar_tabla_carrito()

    def confirmar(self):
        if not self.carrito:
            QMessageBox.information(self, "Carrito vacío", "Agregá al menos un producto antes de confirmar.")
            return

        items = [
            {
                "producto_id": linea["producto"].id,
                "cantidad": linea["cantidad"],
                "precio_unitario": linea["producto"].precio_venta,
            }
            for linea in self.carrito
        ]

        items_ticket = [
            {
                "nombre": linea["producto"].nombre,
                "cantidad": linea["cantidad"],
                "precio_unitario": linea["producto"].precio_venta,
                "subtotal": linea["cantidad"] * linea["producto"].precio_venta,
            }
            for linea in self.carrito
        ]

        try:
            usuario_id = self.usuario_actual.id if self.usuario_actual else None
            venta = confirmar_venta(items, usuario_id=usuario_id)

            caja = QMessageBox(self)
            caja.setWindowTitle("Venta confirmada")
            caja.setText(f"Venta #{venta.id} registrada.\nTotal: ${venta.total:.2f}\n\n¿Querés generar un comprobante?")
            btn_ticket = caja.addButton("🧾 Ticket térmico", QMessageBox.ActionRole)
            btn_a4 = caja.addButton("📄 Hoja A4", QMessageBox.ActionRole)
            caja.addButton("No, gracias", QMessageBox.RejectRole)
            caja.exec()

            boton_elegido = caja.clickedButton()
            if boton_elegido == btn_ticket:
                ruta_pdf = generar_ticket_pdf(venta, items_ticket, formato="ticket")
                os.startfile(ruta_pdf)
            elif boton_elegido == btn_a4:
                ruta_pdf = generar_ticket_pdf(venta, items_ticket, formato="a4")
                os.startfile(ruta_pdf)

            self.vaciar_carrito()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))
    