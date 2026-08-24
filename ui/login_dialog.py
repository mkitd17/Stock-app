from PySide6.QtWidgets import QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QMessageBox
from logica.usuarios_logica import verificar_login


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Iniciar sesión")
        self.resize(300, 150)
        self.usuario_autenticado = None

        layout = QFormLayout(self)

        self.input_usuario = QLineEdit()
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)

        layout.addRow("Usuario:", self.input_usuario)
        layout.addRow("Contraseña:", self.input_password)

        botones = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        botones.accepted.connect(self.intentar_login)
        botones.rejected.connect(self.reject)
        layout.addRow(botones)

    def intentar_login(self):
        nombre = self.input_usuario.text().strip()
        password = self.input_password.text()

        usuario = verificar_login(nombre, password)
        if usuario is None:
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos.")
            return

        self.usuario_autenticado = usuario
        self.accept()