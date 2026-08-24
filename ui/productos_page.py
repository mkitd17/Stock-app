from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QHeaderView,
    QInputDialog
)
from PySide6.QtCore import Qt
from logica.productos_logica import (
    listar_productos, agregar_producto, actualizar_producto,
    eliminar_producto, buscar_por_codigo_exacto
)
from ui.producto_dialog import ProductoDialog


class ProductosPage(QWidget):
    def __init__(self, usuario_actual=None):
        super().__init__()
        self.usuario_actual = usuario_actual
        layout = QVBoxLayout(self)

        # --- Barra superior: buscador + botón agregar ---
        barra_superior = QHBoxLayout()

        self.input_busqueda = QLineEdit()
        self.input_busqueda.setPlaceholderText("Buscar por nombre o código de barras...")
        self.input_busqueda.textChanged.connect(self.actualizar_tabla)

        self.btn_agregar = QPushButton("➕ Nuevo producto")
        self.btn_agregar.clicked.connect(self.abrir_alta)

        barra_superior.addWidget(self.input_busqueda)
        barra_superior.addWidget(self.btn_agregar)
        layout.addLayout(barra_superior)

        # --- Campo de escaneo para reponer stock ---
        barra_scanner = QHBoxLayout()
        self.input_scanner = QLineEdit()
        self.input_scanner.setPlaceholderText("📷 Escanear para reponer stock (o dar de alta si es nuevo)...")
        self.input_scanner.setStyleSheet("font-size: 16px; padding: 6px; border: 2px solid #4CAF50;")
        self.input_scanner.returnPressed.connect(self.procesar_escaneo)
        barra_scanner.addWidget(self.input_scanner)
        layout.addLayout(barra_scanner)

        # --- Tabla ---
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels(
            ["Nombre", "Código", "Categoría", "P. Venta", "Stock", "Stock mín."]
        )
        self.tabla.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.tabla)

        # --- Botones editar/eliminar ---
        barra_inferior = QHBoxLayout()
        self.btn_editar = QPushButton("✏️ Editar seleccionado")
        self.btn_eliminar = QPushButton("🗑️ Eliminar seleccionado")
        self.btn_editar.clicked.connect(self.abrir_edicion)
        self.btn_eliminar.clicked.connect(self.eliminar_seleccionado)
        barra_inferior.addWidget(self.btn_editar)
        barra_inferior.addWidget(self.btn_eliminar)
        layout.addLayout(barra_inferior)

        self.productos_actuales = []
        self.actualizar_tabla()
        self.input_scanner.setFocus()
       
        # Si no es admin, solo puede consultar stock (no modificar)
        if self.usuario_actual and self.usuario_actual.rol != "admin":
            self.btn_agregar.setVisible(False)
            self.btn_editar.setVisible(False)
            self.btn_eliminar.setVisible(False)
            self.input_scanner.setVisible(False)  # el escaneo para reponer stock queda solo para admin

    def actualizar_tabla(self):
        busqueda = self.input_busqueda.text()
        self.productos_actuales = listar_productos(busqueda)

        self.tabla.setRowCount(len(self.productos_actuales))
        for fila, producto in enumerate(self.productos_actuales):
            self.tabla.setItem(fila, 0, QTableWidgetItem(producto.nombre))
            self.tabla.setItem(fila, 1, QTableWidgetItem(producto.codigo_barras or ""))
            nombre_cat = producto.categoria.nombre if producto.categoria else ""
            self.tabla.setItem(fila, 2, QTableWidgetItem(nombre_cat))
            self.tabla.setItem(fila, 3, QTableWidgetItem(f"${producto.precio_venta:.2f}"))
            self.tabla.setItem(fila, 4, QTableWidgetItem(str(producto.stock_actual)))
            self.tabla.setItem(fila, 5, QTableWidgetItem(str(producto.stock_minimo)))

    def fila_seleccionada(self):
        fila = self.tabla.currentRow()
        if fila < 0:
            QMessageBox.information(self, "Sin selección", "Seleccioná un producto primero.")
            return None
        return self.productos_actuales[fila]

    def abrir_alta(self):
        dialogo = ProductoDialog()
        if dialogo.exec():
            datos = dialogo.obtener_valores()
            agregar_producto(**datos)
            self.actualizar_tabla()

    def abrir_edicion(self):
        producto = self.fila_seleccionada()
        if not producto:
            return
        dialogo = ProductoDialog(producto)
        if dialogo.exec():
            datos = dialogo.obtener_valores()
            actualizar_producto(producto.id, **datos)
            self.actualizar_tabla()

    def eliminar_seleccionado(self):
        producto = self.fila_seleccionada()
        if not producto:
            return
        confirmar = QMessageBox.question(
            self, "Confirmar eliminación",
            f"¿Seguro que querés eliminar '{producto.nombre}'?"
        )
        if confirmar == QMessageBox.Yes:
            eliminar_producto(producto.id)
            self.actualizar_tabla()
    def procesar_escaneo(self):
        codigo = self.input_scanner.text().strip()
        self.input_scanner.clear()

        if not codigo:
            return

        producto = buscar_por_codigo_exacto(codigo)

        if producto:
            # Ya existe: preguntamos cuánto stock sumar
            cantidad, ok = QInputDialog.getInt(
                self, "Reponer stock",
                f"'{producto.nombre}' ya existe (stock actual: {producto.stock_actual}).\n¿Cuántas unidades sumar?",
                1, 1, 100000
            )
            if ok:
                nuevo_stock = producto.stock_actual + cantidad
                actualizar_producto(
                    producto.id, producto.nombre, producto.codigo_barras,
                    producto.categoria_id, producto.precio_costo, producto.precio_venta,
                    nuevo_stock, producto.stock_minimo
                )
                self.actualizar_tabla()
        else:
            # No existe: abrimos el alta con el código ya cargado
            dialogo = ProductoDialog()
            dialogo.input_codigo.setText(codigo)
            if dialogo.exec():
                datos = dialogo.obtener_valores()
                agregar_producto(**datos)
                self.actualizar_tabla()