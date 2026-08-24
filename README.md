# StockApp 📦

Aplicación de escritorio moderna para la gestión de inventario, ventas, productos, categorías y facturación, desarrollada en **Python** utilizando **PySide6 (Qt)** para la interfaz gráfica y **SQLAlchemy (SQLite)** para la persistencia de datos.

---

## 🚀 Características principales

*   **Autenticación de Usuarios**: Control de acceso con roles diferenciados (por ejemplo, `admin` y otros roles).
*   **Gestión de Inventario**: Registro, actualización y control de stock de productos y categorías.
*   **Punto de Venta (POS)**: Registro ágil de ventas y emisión automatizada de tickets o facturas.
*   **Generación de Tickets**: Soporte para la impresión o exportación de tickets de venta en formato PDF utilizando `reportlab`.
*   **Base de Datos Autogenerada**: Configuración automatizada de tablas en SQLite en el primer inicio de la aplicación.
*   **Copias de Seguridad (Backups)**: Respaldos automáticos de la base de datos local para evitar pérdidas de información.

---

## 🛠️ Requisitos previos

*   **Python 3.10** o superior instalado en el sistema.
*   Gestor de paquetes **pip**.

---

## 📦 Instalación y Configuración

Sigue estos sencillos pasos para poner en marcha la aplicación en tu entorno de desarrollo local:

### 1. Clonar el repositorio
```bash
git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git
cd TU_REPOSITORIO
```

### 2. Crear y activar un entorno virtual
Es altamente recomendado utilizar un entorno virtual para aislar las dependencias:

*   **En Windows:**
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```
*   **En macOS/Linux:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

### 3. Instalar las dependencias
Instala todas las librerías necesarias con el siguiente comando:
```bash
pip install -r requirements.txt
```

---

## 🖥️ Cómo Ejecutar la Aplicación

Una vez instaladas las dependencias, simplemente ejecuta el script principal:

```bash
python main.py
```

> 💡 **Nota Importante**: Al iniciarse por primera vez, el sistema creará automáticamente la base de datos local `stock.db` y configurará un usuario administrador inicial con las siguientes credenciales:
> *   **Usuario**: `admin`
> *   **Contraseña**: `admin123`
>
> *Se recomienda encarecidamente cambiar esta contraseña o crear un nuevo usuario administrativo desde el panel de control una vez dentro de la aplicación.*

---

## ⚙️ Configuración Personalizada

La aplicación utiliza un archivo llamado `configuracion.json` para gestionar variables de personalización local (como el nombre de tu tienda y la ruta del logo):

```json
{
  "nombre_local": "KR accesorios",
  "ruta_logo": "D:/ruta/a/tu/logo.jpeg"
}
```

---

## 🏛️ Estructura del Proyecto

*   `main.py`: Punto de entrada de la aplicación. Inicializa la base de datos, el entorno, gestiona el login y abre la ventana principal.
*   `crear_db.py`: Script para inicializar/crear la estructura de la base de datos SQLite manualmente.
*   `servidor.py` / `servidor/`: Módulos del servidor o de servicios web relacionados.
*   `modelos/`: Contiene los modelos de datos de SQLAlchemy (`producto.py`, `venta.py`, `usuario.py`, `database.py`).
*   `ui/`: Diseños de interfaz gráfica y diálogos usando PySide6.
*   `logica/`: Lógica de negocio (como backups, gestores de usuarios, etc.).
*   `tickets/`: Lógica o plantillas para la generación de tickets.

---

## 🔨 Compilar a Ejecutable (`.exe` en Windows)

Si deseas empaquetar la aplicación en un archivo ejecutable autónomo utilizando PyInstaller, ejecuta:

```bash
pyinstaller StockApp.spec
```

Esto generará el ejecutable final dentro de la carpeta `dist/`.

---

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Puedes usarlo, modificarlo y distribuirlo libremente.
