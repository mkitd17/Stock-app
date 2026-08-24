from PySide6.QtWidgets import QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QMessageBox
from logica.usuarios_logica import cambiar_password


class CambiarPasswordDialog(QDialog):
    def __init__(self, usuario_actual):
        super().__init__()
        self.usuario_actual = usuario_actual
        self.setWindowTitle("Cambiar contraseña")
        self.resize(320, 180)

        layout = QFormLayout(self)

        self.input_actual = QLineEdit()
        self.input_actual.setEchoMode(QLineEdit.Password)

        self.input_nueva = QLineEdit()
        self.input_nueva.setEchoMode(QLineEdit.Password)

        self.input_confirmar = QLineEdit()
        self.input_confirmar.setEchoMode(QLineEdit.Password)

        layout.addRow("Contraseña actual:", self.input_actual)
        layout.addRow("Contraseña nueva:", self.input_nueva)
        layout.addRow("Confirmar nueva:", self.input_confirmar)

        botones = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        botones.accepted.connect(self.confirmar_cambio)
        botones.rejected.connect(self.reject)
        layout.addRow(botones)

    def confirmar_cambio(self):
        actual = self.input_actual.text()
        nueva = self.input_nueva.text()
        confirmar = self.input_confirmar.text()

        if nueva != confirmar:
            QMessageBox.warning(self, "Error", "La nueva contraseña y su confirmación no coinciden.")
            return

        try:
            cambiar_password(self.usuario_actual.id, actual, nueva)
            QMessageBox.information(self, "Listo", "Contraseña actualizada correctamente.")
            self.accept()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))