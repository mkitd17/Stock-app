ESTILO_APP = """
QWidget {
    background-color: #FBF8F3;
    color: #2C2C2A;
    font-family: Segoe UI;
    font-size: 13px;
}

/* --- Menú lateral --- */
QWidget#menuLateral {
    background-color: #993C1D;
}

QWidget#menuLateral QPushButton {
    background-color: transparent;
    color: #FAECE7;
    border: none;
    text-align: left;
    padding: 10px 12px;
    border-radius: 6px;
}

QWidget#menuLateral QPushButton:hover {
    background-color: #A3441F;
}

QWidget#menuLateral QLabel {
    color: #FAECE7;
}

/* --- Botones generales (fuera del menú) --- */
QPushButton {
    background-color: #FFFFFF;
    border: 1px solid #E0DCD3;
    border-radius: 6px;
    padding: 8px 14px;
}

QPushButton:hover {
    background-color: #F5EFE4;
    border: 1px solid #D85A30;
}

QPushButton:pressed {
    background-color: #F0997B;
}

/* --- Campos de texto --- */
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {
    background-color: #FFFFFF;
    border: 1px solid #E0DCD3;
    border-radius: 6px;
    padding: 6px 8px;
}

QLineEdit:focus, QComboBox:focus {
    border: 1px solid #D85A30;
}

/* --- Tablas --- */
QTableWidget {
    background-color: #FFFFFF;
    border: 1px solid #E0DCD3;
    border-radius: 6px;
    gridline-color: #F0EBE1;
}

QHeaderView::section {
    background-color: #FAECE7;
    color: #4A1B0C;
    padding: 6px;
    border: none;
    font-weight: bold;
}

QTableWidget::item:selected {
    background-color: #F0997B;
    color: #4A1B0C;
}

/* --- GroupBox (usado en Reportes) --- */
QGroupBox {
    background-color: #FFFFFF;
    border: 1px solid #E0DCD3;
    border-radius: 8px;
    margin-top: 10px;
    padding-top: 10px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    color: #993C1D;
    font-weight: bold;
}
"""