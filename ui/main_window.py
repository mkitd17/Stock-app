from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QStackedWidget, QLabel
)
from ui.productos_page import ProductosPage
from ui.ventas_page import VentasPage
from ui.reportes_page import ReportesPage
from ui.configuracion_dialog import ConfiguracionDialog
from PySide6.QtCore import QTimer
from logica.backup_logica import crear_backup
from ui.usuarios_page import UsuariosPage
from ui.ventas_historial_page import VentasHistorialPage
from ui.cambiar_password_dialog import CambiarPasswordDialog

class MainWindow(QMainWindow):
    def __init__(self, usuario_actual):
        super().__init__()
        self.usuario_actual = usuario_actual
        self.setWindowTitle("Stock App")
        self.resize(1000, 650)

        # Widget central que contiene todo
        contenedor = QWidget()
        self.setCentralWidget(contenedor)
        layout_principal = QHBoxLayout(contenedor)

        # --- Menú lateral ---
        menu_lateral = QWidget()
        menu_lateral.setFixedWidth(180)
        menu_lateral.setObjectName("menuLateral")
        menu_layout = QVBoxLayout(menu_lateral)

        self.btn_productos = QPushButton("📦 Productos")
        self.btn_ventas = QPushButton("💰 Ventas")
        self.btn_reportes = QPushButton("📊 Reportes")
        self.btn_configuracion = QPushButton("⚙️ Configuración")
        self.btn_backup = QPushButton("💾 Backups")
        self.btn_usuarios = QPushButton("👥 Usuarios")
        self.btn_historial = QPushButton("🧾 Historial de ventas")

        for btn in (self.btn_productos, self.btn_ventas, self.btn_reportes, self.btn_configuracion, self.btn_backup, self.btn_usuarios, self.btn_historial):
            btn.setMinimumHeight(45)
            menu_layout.addWidget(btn)

        self.btn_configuracion.clicked.connect(self.abrir_configuracion)
        etiqueta_usuario = QLabel(f"👤 {self.usuario_actual.nombre_usuario}\n({self.usuario_actual.rol})")
        etiqueta_usuario.setStyleSheet("color: gray; font-size: 11px; padding: 10px;")
        self.btn_cambiar_password = QPushButton("🔑 Cambiar contraseña")
        self.btn_cambiar_password.clicked.connect(self.abrir_cambiar_password)
        menu_layout.addWidget(self.btn_cambiar_password)
        menu_layout.addWidget(etiqueta_usuario)

        menu_layout.addStretch()  # empuja los botones hacia arriba

        # --- Área de contenido (cambia según el botón que apretes) ---
        self.contenido = QStackedWidget()

        # Por ahora, páginas de prueba (después las reemplazamos por las reales)
        self.pagina_productos = ProductosPage(usuario_actual=self.usuario_actual)
        self.pagina_ventas = VentasPage(usuario_actual=self.usuario_actual)
        self.pagina_reportes = ReportesPage()
        self.pagina_usuarios = UsuariosPage()
        self.pagina_historial = VentasHistorialPage()

        for pagina in (self.pagina_productos, self.pagina_ventas, self.pagina_reportes, self.pagina_usuarios, self.pagina_historial):
            pagina.setStyleSheet("font-size: 18px; padding: 20px;")
            self.contenido.addWidget(pagina)

        # Conectar botones con el cambio de página
        self.btn_productos.clicked.connect(lambda: self.contenido.setCurrentWidget(self.pagina_productos))
        self.btn_ventas.clicked.connect(lambda: self.contenido.setCurrentWidget(self.pagina_ventas))
        self.btn_reportes.clicked.connect(self.ir_a_reportes)
        self.btn_usuarios.clicked.connect(lambda: self.contenido.setCurrentWidget(self.pagina_usuarios))
        self.btn_historial.clicked.connect(lambda: self.contenido.setCurrentWidget(self.pagina_historial))

        # Armar el layout final
        layout_principal.addWidget(menu_lateral)
        layout_principal.addWidget(self.contenido)

        # --- Backup automático periódico ---
        self.timer_backup = QTimer(self)
        self.timer_backup.timeout.connect(self.backup_automatico_silencioso)
        INTERVALO_BACKUP_MS = 30 * 60 * 1000  # cada 30 minutos
        self.timer_backup.start(INTERVALO_BACKUP_MS)

        # Si no es admin, solo puede ver Ventas
        if self.usuario_actual.rol != "admin":
            self.btn_reportes.setVisible(False)
            self.btn_configuracion.setVisible(False)
            self.btn_backup.setVisible(False)
            self.btn_usuarios.setVisible(False)
            self.btn_historial.setVisible(False)
            self.contenido.setCurrentWidget(self.pagina_ventas)

    def ir_a_reportes(self):
        self.contenido.setCurrentWidget(self.pagina_reportes)
        self.pagina_reportes.actualizar_todo()
    def abrir_configuracion(self):
        dialogo = ConfiguracionDialog()
        dialogo.exec()
    def abrir_cambiar_password(self):
        dialogo = CambiarPasswordDialog(self.usuario_actual)
        dialogo.exec()
    def backup_automatico_silencioso(self):
        """Genera un backup sin mostrar ningún mensaje, para no interrumpir al usuario."""
        crear_backup()
    def closeEvent(self, event):
        """Se ejecuta automáticamente cuando el usuario cierra la ventana."""
        crear_backup()
        event.accept()