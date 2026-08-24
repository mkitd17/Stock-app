import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from modelos.database import engine, Base
from modelos.producto import Categoria, Producto
from modelos.venta import Venta, DetalleVenta
from modelos.usuario import Usuario
from ui.main_window import MainWindow
from ui.login_dialog import LoginDialog
from logica.backup_logica import crear_backup
from logica.usuarios_logica import existe_algun_usuario, crear_usuario
from ui.estilos import ESTILO_APP

# Crea las tablas si no existen (primera vez que se abre la app en esta PC)
Base.metadata.create_all(engine)

crear_backup()

app = QApplication(sys.argv)
app.setStyleSheet(ESTILO_APP)

# Si es la primera vez que se usa la app, se crea un usuario admin automáticamente
if not existe_algun_usuario():
    crear_usuario("admin", "admin123", rol="admin")
    QMessageBox.information(
        None, "Usuario creado",
        "Se creó un usuario administrador inicial:\n\n"
        "Usuario: admin\nContraseña: admin123\n\n"
        "Te recomendamos crear tu propio usuario y cambiar esta contraseña luego."
    )

login = LoginDialog()
if login.exec():
    ventana = MainWindow(usuario_actual=login.usuario_autenticado)
    ventana.show()
    app.exec()
else:
    sys.exit()