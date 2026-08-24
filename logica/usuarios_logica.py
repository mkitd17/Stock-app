import hashlib
import os
from modelos.database import SessionLocal
from modelos.usuario import Usuario


def _generar_hash(password: str, salt: bytes = None):
    if salt is None:
        salt = os.urandom(16)
    hash_bytes = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100_000)
    return hash_bytes.hex(), salt.hex()


def crear_usuario(nombre_usuario, password, rol="vendedor"):
    db = SessionLocal()
    if db.query(Usuario).filter(Usuario.nombre_usuario == nombre_usuario).first():
        db.close()
        raise ValueError("Ya existe un usuario con ese nombre.")

    password_hash, salt = _generar_hash(password)
    usuario = Usuario(nombre_usuario=nombre_usuario, password_hash=password_hash, salt=salt, rol=rol)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    db.close()
    return usuario


def verificar_login(nombre_usuario, password):
    db = SessionLocal()
    usuario = db.query(Usuario).filter(
        Usuario.nombre_usuario == nombre_usuario, Usuario.activo == True
    ).first()
    db.close()

    if usuario is None:
        return None

    hash_calculado, _ = _generar_hash(password, bytes.fromhex(usuario.salt))
    if hash_calculado == usuario.password_hash:
        return usuario
    return None


def listar_usuarios():
    db = SessionLocal()
    usuarios = db.query(Usuario).order_by(Usuario.nombre_usuario).all()
    db.close()
    return usuarios


def existe_algun_usuario():
    db = SessionLocal()
    existe = db.query(Usuario).first() is not None
    db.close()
    return existe


def desactivar_usuario(usuario_id):
    db = SessionLocal()
    usuario = db.query(Usuario).get(usuario_id)
    if usuario:
        usuario.activo = False
        db.commit()
    db.close()

def cambiar_password(usuario_id, password_actual, password_nueva):
    db = SessionLocal()
    usuario = db.query(Usuario).get(usuario_id)
    if usuario is None:
        db.close()
        raise ValueError("Usuario no encontrado.")

    hash_actual, _ = _generar_hash(password_actual, bytes.fromhex(usuario.salt))
    if hash_actual != usuario.password_hash:
        db.close()
        raise ValueError("La contraseña actual no es correcta.")

    if len(password_nueva) < 4:
        db.close()
        raise ValueError("La nueva contraseña debe tener al menos 4 caracteres.")

    nuevo_hash, nuevo_salt = _generar_hash(password_nueva)
    usuario.password_hash = nuevo_hash
    usuario.salt = nuevo_salt
    db.commit()
    db.close()
def usuario_tiene_ventas(usuario_id):
    from modelos.venta import Venta
    db = SessionLocal()
    tiene = db.query(Venta).filter(Venta.usuario_id == usuario_id).first() is not None
    db.close()
    return tiene


def eliminar_usuario(usuario_id):
    if usuario_tiene_ventas(usuario_id):
        raise ValueError("Este usuario ya tiene ventas registradas. Para conservar el historial, desactivalo en vez de eliminarlo.")

    db = SessionLocal()
    usuario = db.query(Usuario).get(usuario_id)
    if usuario:
        db.delete(usuario)
        db.commit()
    db.close()