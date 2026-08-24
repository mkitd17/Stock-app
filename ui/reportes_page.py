from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QGroupBox
)
from PySide6.QtCore import Qt
from logica.reportes_logica import (
    resumen_periodo, productos_mas_vendidos, productos_stock_bajo,
    rango_hoy, rango_ultimos_dias
)


class ReportesPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        # --- Selector de período ---
        barra_periodo = QHBoxLayout()
        self.btn_hoy = QPushButton("Hoy")
        self.btn_7dias = QPushButton("Últimos 7 días")
        self.btn_30dias = QPushButton("Últimos 30 días")

        self.btn_hoy.clicked.connect(lambda: self.cambiar_periodo(*rango_hoy()))
        self.btn_7dias.clicked.connect(lambda: self.cambiar_periodo(*rango_ultimos_dias(7)))
        self.btn_30dias.clicked.connect(lambda: self.cambiar_periodo(*rango_ultimos_dias(30)))

        barra_periodo.addWidget(self.btn_hoy)
        barra_periodo.addWidget(self.btn_7dias)
        barra_periodo.addWidget(self.btn_30dias)
        barra_periodo.addStretch()
        layout.addLayout(barra_periodo)

        # --- Resumen (total y cantidad de ventas) ---
        grupo_resumen = QGroupBox("Resumen del período")
        layout_resumen = QHBoxLayout(grupo_resumen)

        self.label_total = QLabel("Total: $0.00")
        self.label_total.setStyleSheet("font-size: 22px; font-weight: bold;")
        self.label_cantidad = QLabel("Ventas: 0")
        self.label_cantidad.setStyleSheet("font-size: 16px; color: gray;")

        layout_resumen.addWidget(self.label_total)
        layout_resumen.addStretch()
        layout_resumen.addWidget(self.label_cantidad)
        layout.addWidget(grupo_resumen)

        # --- Ranking de productos más vendidos ---
        layout.addWidget(QLabel("🏆 Productos más vendidos"))
        self.tabla_ranking = QTableWidget()
        self.tabla_ranking.setColumnCount(3)
        self.tabla_ranking.setHorizontalHeaderLabels(["Producto", "Unidades vendidas", "Total facturado"])
        self.tabla_ranking.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tabla_ranking.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.tabla_ranking)

        # --- Alerta de stock bajo ---
        layout.addWidget(QLabel("⚠️ Productos con stock bajo (repone pronto)"))
        self.tabla_stock_bajo = QTableWidget()
        self.tabla_stock_bajo.setColumnCount(3)
        self.tabla_stock_bajo.setHorizontalHeaderLabels(["Producto", "Stock actual", "Stock mínimo"])
        self.tabla_stock_bajo.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tabla_stock_bajo.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.tabla_stock_bajo)

        self.desde_actual = None
        self.hasta_actual = None
        self.cambiar_periodo(*rango_hoy())

    def cambiar_periodo(self, desde, hasta):
        self.desde_actual = desde
        self.hasta_actual = hasta
        self.actualizar_todo()

    def actualizar_todo(self):
        # Resumen
        resumen = resumen_periodo(self.desde_actual, self.hasta_actual)
        self.label_total.setText(f"Total: ${resumen['total']:.2f}")
        self.label_cantidad.setText(f"Ventas: {resumen['cantidad_ventas']}")

        # Ranking
        ranking = productos_mas_vendidos(self.desde_actual, self.hasta_actual)
        self.tabla_ranking.setRowCount(len(ranking))
        for fila, (nombre, unidades, total) in enumerate(ranking):
            self.tabla_ranking.setItem(fila, 0, QTableWidgetItem(nombre))
            self.tabla_ranking.setItem(fila, 1, QTableWidgetItem(str(unidades)))
            self.tabla_ranking.setItem(fila, 2, QTableWidgetItem(f"${total:.2f}"))

        # Stock bajo
        bajos = productos_stock_bajo()
        self.tabla_stock_bajo.setRowCount(len(bajos))
        for fila, producto in enumerate(bajos):
            self.tabla_stock_bajo.setItem(fila, 0, QTableWidgetItem(producto.nombre))
            self.tabla_stock_bajo.setItem(fila, 1, QTableWidgetItem(str(producto.stock_actual)))
            self.tabla_stock_bajo.setItem(fila, 2, QTableWidgetItem(str(producto.stock_minimo)))