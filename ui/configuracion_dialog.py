from PySide6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QPushButton, QDialogButtonBox,
    QFileDialog, QHBoxLayout, QLabel
)
from logica.config_logica import obtener_configuracion, guardar_configuracion


class ConfiguracionDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configuración del local")
        self.resize(420, 150)

        layout = QFormLayout(self)
        config = obtener_configuracion()

        self.input_nombre = QLineEdit(config["nombre_local"])
        layout.addRow("Nombre del local:", self.input_nombre)

        self.ruta_logo = config["ruta_logo"]
        fila_logo = QHBoxLayout()
        self.label_logo = QLabel(self.ruta_logo or "Sin logo seleccionado")
        self.label_logo.setStyleSheet("color: gray; font-size: 11px;")
        btn_elegir = QPushButton("Elegir imagen...")
        btn_elegir.clicked.connect(self.elegir_logo)
        fila_logo.addWidget(self.label_logo)
        fila_logo.addWidget(btn_elegir)
        layout.addRow("Logo:", fila_logo)

        botones = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        botones.accepted.connect(self.guardar)
        botones.rejected.connect(self.reject)
        layout.addRow(botones)

    def elegir_logo(self):
        ruta, _ = QFileDialog.getOpenFileName(self, "Seleccionar logo", "", "Imágenes (*.png *.jpg *.jpeg)")
        if ruta:
            self.ruta_logo = ruta
            self.label_logo.setText(ruta)

    def guardar(self):
        guardar_configuracion(self.input_nombre.text().strip(), self.ruta_logo)
        self.accept()