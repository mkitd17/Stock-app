from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView
)
from logica.usuarios_logica import crear_usuario, listar_usuarios, desactivar_usuario
from logica.usuarios_logica import crear_usuario, listar_usuarios, desactivar_usuario, eliminar_usuario

class UsuariosPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        # --- Formulario para crear usuario nuevo ---
        formulario = QHBoxLayout()

        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Nombre de usuario")

        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Contraseña")
        self.input_password.setEchoMode(QLineEdit.Password)

        self.combo_rol = QComboBox()
        self.combo_rol.addItem("Vendedor", "vendedor")
        self.combo_rol.addItem("Admin", "admin")

        self.btn_crear = QPushButton("➕ Crear usuario")
        self.btn_crear.clicked.connect(self.crear)

        formulario.addWidget(self.input_nombre)
        formulario.addWidget(self.input_password)
        formulario.addWidget(self.combo_rol)
        formulario.addWidget(self.btn_crear)
        layout.addLayout(formulario)

        # --- Tabla de usuarios existentes ---
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(3)
        self.tabla.setHorizontalHeaderLabels(["Usuario", "Rol", "Estado"])
        self.tabla.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.tabla)

        self.btn_desactivar = QPushButton("🚫 Desactivar usuario seleccionado")
        self.btn_desactivar.clicked.connect(self.desactivar_seleccionado)
        layout.addWidget(self.btn_desactivar)

        self.btn_eliminar = QPushButton("🗑️ Eliminar usuario seleccionado")
        self.btn_eliminar.clicked.connect(self.eliminar_seleccionado)
        layout.addWidget(self.btn_eliminar)

        self.usuarios_actuales = []
        self.actualizar_tabla()

    def actualizar_tabla(self):
        self.usuarios_actuales = listar_usuarios()
        self.tabla.setRowCount(len(self.usuarios_actuales))
        for fila, usuario in enumerate(self.usuarios_actuales):
            self.tabla.setItem(fila, 0, QTableWidgetItem(usuario.nombre_usuario))
            self.tabla.setItem(fila, 1, QTableWidgetItem(usuario.rol))
            estado = "Activo" if usuario.activo else "Desactivado"
            self.tabla.setItem(fila, 2, QTableWidgetItem(estado))

    def crear(self):
        nombre = self.input_nombre.text().strip()
        password = self.input_password.text()
        rol = self.combo_rol.currentData()

        if not nombre or not password:
            QMessageBox.warning(self, "Faltan datos", "Completá usuario y contraseña.")
            return

        try:
            crear_usuario(nombre, password, rol)
            QMessageBox.information(self, "Usuario creado", f"Se creó el usuario '{nombre}' correctamente.")
            self.input_nombre.clear()
            self.input_password.clear()
            self.actualizar_tabla()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    def desactivar_seleccionado(self):
        fila = self.tabla.currentRow()
        if fila < 0:
            QMessageBox.information(self, "Sin selección", "Seleccioná un usuario primero.")
            return

        usuario = self.usuarios_actuales[fila]
        confirmar = QMessageBox.question(
            self, "Confirmar",
            f"¿Desactivar al usuario '{usuario.nombre_usuario}'? No podrá volver a iniciar sesión."
        )
        if confirmar == QMessageBox.Yes:
            desactivar_usuario(usuario.id)
            self.actualizar_tabla()
    def eliminar_seleccionado(self):
        fila = self.tabla.currentRow()
        if fila < 0:
            QMessageBox.information(self, "Sin selección", "Seleccioná un usuario primero.")
            return

        usuario = self.usuarios_actuales[fila]
        confirmar = QMessageBox.warning(
            self, "Confirmar eliminación",
            f"¿Eliminar definitivamente al usuario '{usuario.nombre_usuario}'?\n\nEsta acción no se puede deshacer.",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirmar == QMessageBox.Yes:
            try:
                eliminar_usuario(usuario.id)
                QMessageBox.information(self, "Eliminado", "El usuario fue eliminado correctamente.")
                self.actualizar_tabla()
            except ValueError as e:
                QMessageBox.warning(self, "No se puede eliminar", str(e))