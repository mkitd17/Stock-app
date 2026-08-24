from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QMessageBox, QHeaderView, QLabel
)
from logica.ventas_logica import listar_ventas_recientes, anular_venta


class VentasHistorialPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Últimas ventas registradas"))

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(["ID", "Fecha", "Vendedor", "Total", "Estado"])
        self.tabla.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.tabla)

        barra_botones = QHBoxLayout()
        self.btn_actualizar = QPushButton("🔄 Actualizar")
        self.btn_anular = QPushButton("❌ Anular venta seleccionada")
        self.btn_actualizar.clicked.connect(self.actualizar_tabla)
        self.btn_anular.clicked.connect(self.anular_seleccionada)
        barra_botones.addWidget(self.btn_actualizar)
        barra_botones.addWidget(self.btn_anular)
        layout.addLayout(barra_botones)

        self.ventas_actuales = []
        self.actualizar_tabla()

    def actualizar_tabla(self):
        self.ventas_actuales = listar_ventas_recientes()
        self.tabla.setRowCount(len(self.ventas_actuales))

        for fila, venta in enumerate(self.ventas_actuales):
            self.tabla.setItem(fila, 0, QTableWidgetItem(str(venta.id)))
            self.tabla.setItem(fila, 1, QTableWidgetItem(venta.fecha.strftime("%d/%m/%Y %H:%M")))
            nombre_vendedor = venta.usuario.nombre_usuario if venta.usuario else "—"
            self.tabla.setItem(fila, 2, QTableWidgetItem(nombre_vendedor))
            self.tabla.setItem(fila, 3, QTableWidgetItem(f"${venta.total:.2f}"))
            estado = "❌ Anulada" if venta.anulada else "✅ Activa"
            self.tabla.setItem(fila, 4, QTableWidgetItem(estado))

    def anular_seleccionada(self):
        fila = self.tabla.currentRow()
        if fila < 0:
            QMessageBox.information(self, "Sin selección", "Seleccioná una venta primero.")
            return

        venta = self.ventas_actuales[fila]

        if venta.anulada:
            QMessageBox.information(self, "Ya anulada", "Esta venta ya estaba anulada.")
            return

        confirmar = QMessageBox.warning(
            self, "Confirmar anulación",
            f"¿Anular la venta #{venta.id} por ${venta.total:.2f}?\n\n"
            "El stock de los productos vendidos se va a devolver automáticamente.",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirmar == QMessageBox.Yes:
            try:
                anular_venta(venta.id)
                QMessageBox.information(self, "Venta anulada", "La venta se anuló y el stock fue restituido.")
                self.actualizar_tabla()
            except ValueError as e:
                QMessageBox.warning(self, "Error", str(e))