from PySide6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QComboBox, QDoubleSpinBox,
    QSpinBox, QDialogButtonBox, QMessageBox, QHBoxLayout, QPushButton,
    QInputDialog
)
from logica.productos_logica import obtener_categorias, crear_categoria


class ProductoDialog(QDialog):
    def __init__(self, producto=None):
        super().__init__()
        self.producto = producto  # si viene un producto, es edición; si no, es alta
        self.setWindowTitle("Editar producto" if producto else "Nuevo producto")
        self.resize(350, 300)

        layout = QFormLayout(self)

        self.input_nombre = QLineEdit()
        self.input_codigo = QLineEdit()

        self.combo_categoria = QComboBox()
        self.categorias = obtener_categorias()
        for cat in self.categorias:
            self.combo_categoria.addItem(cat.nombre, cat.id)

        self.input_costo = QDoubleSpinBox()
        self.input_costo.setMaximum(1_000_000)
        self.input_costo.setPrefix("$ ")

        self.input_venta = QDoubleSpinBox()
        self.input_venta.setMaximum(1_000_000)
        self.input_venta.setPrefix("$ ")

        self.input_stock = QSpinBox()
        self.input_stock.setMaximum(1_000_000)

        self.input_stock_min = QSpinBox()
        self.input_stock_min.setMaximum(1_000_000)

        self.btn_nueva_categoria = QPushButton("➕")
        self.btn_nueva_categoria.setFixedWidth(30)
        self.btn_nueva_categoria.clicked.connect(self.agregar_categoria_rapida)

        fila_categoria = QHBoxLayout()
        fila_categoria.addWidget(self.combo_categoria)
        fila_categoria.addWidget(self.btn_nueva_categoria)

        layout.addRow("Nombre:", self.input_nombre)
        layout.addRow("Código de barras:", self.input_codigo)
        layout.addRow("Categoría:", fila_categoria)
        layout.addRow("Precio costo:", self.input_costo)
        layout.addRow("Precio venta:", self.input_venta)
        layout.addRow("Stock actual:", self.input_stock)
        layout.addRow("Stock mínimo:", self.input_stock_min)

        botones = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        botones.accepted.connect(self.validar_y_aceptar)
        botones.rejected.connect(self.reject)
        layout.addRow(botones)

        if producto:
            self.cargar_datos(producto)

    def cargar_datos(self, producto):
        self.input_nombre.setText(producto.nombre)
        self.input_codigo.setText(producto.codigo_barras or "")
        self.input_costo.setValue(producto.precio_costo)
        self.input_venta.setValue(producto.precio_venta)
        self.input_stock.setValue(producto.stock_actual)
        self.input_stock_min.setValue(producto.stock_minimo)
        if producto.categoria_id:
            index = self.combo_categoria.findData(producto.categoria_id)
            if index >= 0:
                self.combo_categoria.setCurrentIndex(index)
    def agregar_categoria_rapida(self):
        nombre, ok = QInputDialog.getText(self, "Nueva categoría", "Nombre de la categoría:")
        if ok and nombre.strip():
            nueva = crear_categoria(nombre)
            self.combo_categoria.addItem(nueva.nombre, nueva.id)
            self.combo_categoria.setCurrentIndex(self.combo_categoria.count() - 1)

    def validar_y_aceptar(self):
        if not self.input_nombre.text().strip():
            QMessageBox.warning(self, "Falta información", "El nombre es obligatorio.")
            return
        self.accept()

    def obtener_valores(self):
        return {
            "nombre": self.input_nombre.text().strip(),
            "codigo_barras": self.input_codigo.text().strip(),
            "categoria_id": self.combo_categoria.currentData(),
            "precio_costo": self.input_costo.value(),
            "precio_venta": self.input_venta.value(),
            "stock_actual": self.input_stock.value(),
            "stock_minimo": self.input_stock_min.value(),
        }