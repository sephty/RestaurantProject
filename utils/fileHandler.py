import json
import os

def load_json(filename):
    """Carga datos desde un archivo JSON, manejando errores de forma segura y validando la estructura."""
    try:
        if not os.path.exists(filename):
            print(f"Advertencia: Archivo {filename} no encontrado. Creando archivo vacío.")
            return None

        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Validar estructura básica
        if not isinstance(data, dict):
            print(f"Error: Estructura inválida en {filename}. Debe ser un objeto JSON.")
            return None

        return data

    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo {filename}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Archivo {filename} contiene JSON inválido: {e}")
        return None
    except PermissionError:
        print(f"Error: No hay permisos para leer el archivo {filename}")
        return None
    except Exception as e:
        print(f"Error inesperado al cargar {filename}: {e}")
        return None
    
        
def validar_entero(mensaje, min_val=None, max_val=None, permitir_vacio=False):
    """Valida entrada de número entero con límites opcionales."""
    while True:
        try:
            entrada = input(mensaje).strip()
            if permitir_vacio and entrada == "":
                return None
            valor = int(entrada)
            if min_val is not None and valor < min_val:
                print(f"Error: El valor debe ser al menos {min_val}")
                continue
            if max_val is not None and valor > max_val:
                print(f"Error: El valor debe ser como máximo {max_val}")
                continue
            return valor
        except ValueError:
            print("Error: Por favor ingrese un número entero válido")

def validar_opcion_menu(opciones_validas):
    """Valida que la opción del menú esté en la lista de opciones válidas."""
    while True:
        opcion = input("Seleccione una opción: ").strip()
        if opcion in opciones_validas:
            return opcion
        print(f"Error: Opción inválida. Opciones válidas: {', '.join(opciones_validas)}")

def validar_codigo_producto(codigo):
    """Valida que un código de producto tenga el formato correcto."""
    if not codigo or len(codigo) < 2:
        return False
    if not codigo[0].isalpha() or not codigo[1:].isdigit():
        return False
    return True

def validar_datos_cliente(cliente_data):
    """Valida la estructura de datos de clientes."""
    if not isinstance(cliente_data, dict) or "clientes" not in cliente_data:
        return False
    if not isinstance(cliente_data["clientes"], list):
        return False
    return True

def validar_datos_productos(productos):
    """Valida la estructura de datos de productos."""
    if not isinstance(productos, dict):
        return False
    categorias_esperadas = ["pizzas", "bebidas", "toppings", "adiciones", "salsas"]
    for categoria in categorias_esperadas:
        if categoria not in productos:
            productos[categoria] = []
        elif not isinstance(productos[categoria], list):
            return False
    return True

def save_json(filename, data):
    """Guarda datos en un archivo JSON con formato legible, validando la serialización."""
    try:
        # Validar que data sea serializable
        if data is not None:
            json.dumps(data, ensure_ascii=False)  # Test serialization

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    except TypeError as e:
        print(f"Error: Los datos no son serializables a JSON: {e}")
        raise
    except PermissionError:
        print(f"Error: No hay permisos para escribir en {filename}")
        raise
    except Exception as e:
        print(f"Error inesperado al guardar {filename}: {e}")
        raise

def limpiarPantalla():
    input("Presione Enter para continuar...")
    os.system('cls' if os.name == 'nt' else 'clear')

def recargarProductos():
    """Recarga los productos desde el archivo JSON."""
    global productos
    productos = load_json(PRODUCT_FILE) or {"pizzas": [], "bebidas": [], "toppings": [], "salsas": []}

def get_product_by_code(code):
    """Obtiene un producto por su código."""
    recargarDatos()
    for categoria in productos.values():
        for item in categoria:
            if item["code"] == code:
                return item
    return None

def get_next_code(tipo):
    """Genera el siguiente código disponible para un tipo de producto."""
    recargarDatos()
    if tipo == "pizza":
        existing = [p["code"] for p in productos["pizzas"]]
        prefix = "P"
    elif tipo == "bebida":
        existing = [b["code"] for b in productos["bebidas"]]
        prefix = "B"
    elif tipo == "adicion":
        existing = [a["code"] for a in productos["adiciones"]]
        prefix = "A"
    elif tipo == "topping":
        existing = [t["code"] for t in productos["toppings"]]
        prefix = "T"
    elif tipo == "salsa":
        existing = [s["code"] for s in productos["salsas"]]
        prefix = "S"
    else:
        return None
    numbers = [int(code[1:]) for code in existing if code.startswith(prefix) and code[1:].isdigit()]
    next_num = max(numbers) + 1 if numbers else 1
    return f"{prefix}{next_num:03d}"
