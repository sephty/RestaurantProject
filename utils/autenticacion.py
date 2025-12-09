"""
Módulo de autenticación y gestión de usuarios.
"""

from utils.fileHandler import load_json, save_json
from utils.path import CLIENT_FILE

usuario_actual = None
cliente_data = load_json(CLIENT_FILE) or {"clientes": []}

def recargarDatos():
    """Recarga los datos de clientes desde el archivo JSON."""
    global cliente_data
    cliente_data = load_json(CLIENT_FILE) or {"clientes": []}

def esAdmin():
    """Verifica si el usuario actual es administrador."""
    global usuario_actual
    if usuario_actual is None:
        return False
    return usuario_actual.get("admin", False)

def iniciarSesion():
    """Permite al usuario iniciar sesión o registrarse."""
    global usuario_actual, cliente_data
    recargarDatos()

    import os
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== Iniciar Sesión - Pizzería ===")
    print("1. Iniciar sesión con cuenta existente")
    print("2. Registrar nueva cuenta")
    print("0. Continuar sin cuenta")

    opcion = input("Seleccione una opción: ")

    if opcion == '1':
        nombre = input("Ingrese su nombre de usuario: ")
        for cliente in cliente_data["clientes"]:
            if cliente["nombre"].lower() == nombre.lower():
                usuario_actual = cliente
                print(f"Bienvenido de nuevo, {cliente['nombre']}!")
                if esAdmin():
                    print("(Cuenta de administrador)")
                return True
        print("Usuario no encontrado.")
        return False

    elif opcion == '2':
        nombre = input("Ingrese el nombre para su nueva cuenta: ")
        # Verificar que no exista
        for cliente in cliente_data["clientes"]:
            if cliente["nombre"].lower() == nombre.lower():
                print("Este nombre de usuario ya existe.")
                return False

        new_id = len(cliente_data["clientes"]) + 1
        new_cliente = {
            "id": new_id,
            "nombre": nombre,
            "admin": False,
            "pedidos": []
        }
        cliente_data["clientes"].append(new_cliente)
        save_json(CLIENT_FILE, cliente_data)
        usuario_actual = new_cliente
        print(f"Cuenta creada exitosamente. Bienvenido, {nombre}!")
        return True

    elif opcion == '0':
        usuario_actual = None
        print("Continuando sin cuenta...")
        return True

    return False

def cerrarSesion():
    """Cierra la sesión del usuario actual."""
    global usuario_actual
    if usuario_actual:
        print(f"Hasta luego, {usuario_actual['nombre']}!")
    usuario_actual = None

def obtenerUsuarioActual():
    """Retorna el usuario actualmente logueado."""
    return usuario_actual
