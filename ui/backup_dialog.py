from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton,
    QLabel, QMessageBox
)
from logica.backup_logica import crear_backup, listar_backups, restaurar_backup


class BackupDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Copias de seguridad")
        self.resize(450, 400)

        layout = QVBoxLayout(self)

        info = QLabel("Se genera un backup automático cada vez que abrís la app.\nTambién podés generar uno manual cuando quieras.")
        info.setStyleSheet("color: gray; font-size: 11px;")
        layout.addWidget(info)

        self.btn_backup_ahora = QPushButton("💾 Hacer backup ahora")
        self.btn_backup_ahora.clicked.connect(self.hacer_backup_ahora)
        layout.addWidget(self.btn_backup_ahora)

        layout.addWidget(QLabel("Backups disponibles (el más reciente arriba):"))

        self.lista_backups = QListWidget()
        layout.addWidget(self.lista_backups)

        self.btn_restaurar = QPushButton("♻️ Restaurar backup seleccionado")
        self.btn_restaurar.clicked.connect(self.restaurar_seleccionado)
        layout.addWidget(self.btn_restaurar)

        self.actualizar_lista()

    def actualizar_lista(self):
        self.lista_backups.clear()
        for nombre in listar_backups():
            self.lista_backups.addItem(nombre)

    def hacer_backup_ahora(self):
        ruta = crear_backup()
        if ruta:
            QMessageBox.information(self, "Backup creado", "Se generó una copia de seguridad correctamente.")
            self.actualizar_lista()
        else:
            QMessageBox.warning(self, "Error", "No se encontró la base de datos para respaldar.")

    def restaurar_seleccionado(self):
        item = self.lista_backups.currentItem()
        if item is None:
            QMessageBox.information(self, "Sin selección", "Seleccioná un backup de la lista primero.")
            return

        confirmar = QMessageBox.warning(
            self, "Confirmar restauración",
            f"Esto va a REEMPLAZAR la base de datos actual por:\n\n{item.text()}\n\n"
            "Se guardará un backup de la base actual antes de restaurar, por las dudas.\n"
            "¿Continuar?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirmar == QMessageBox.Yes:
            exito = restaurar_backup(item.text())
            if exito:
                QMessageBox.information(
                    self, "Restaurado",
                    "Backup restaurado correctamente.\nCerrá y volvé a abrir la app para ver los cambios."
                )
                self.actualizar_lista()
            else:
                QMessageBox.warning(self, "Error", "No se pudo restaurar el backup seleccionado.")