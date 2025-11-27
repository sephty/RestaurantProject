from utils.fileHandler import load_json, save_json
from utils.path import CLIENT_FILE, PRODUCT_FILE

productos = load_json(CLIENT_FILE) or {"platillos": [], "bebidas": [], "adiciones": []}
cliente_data = load_json(PRODUCT_FILE) or {"clientes": []}
    
def menuPizzas():
    print("=== Menú de Platillos ===")
    platillos = productos["platillos"]
    for i, platillo in enumerate(platillos):
        print(f"{i + 1}. {platillo['nombre']} - ${platillo['precio']}")

    opcion = input(f"Seleccione un platillo (1-{len(platillos)}): ")

    try:
        index = int(opcion) - 1
        if 0 <= index < len(platillos):
            item = platillos[index]
            print(f"Ha seleccionado {item['nombre']}.")
            return (f"{item['nombre']} - ${item['precio']}", item['precio'])
        else:
            print("Opción inválida.")
            return None
    except ValueError:
        print("Opción inválida.")
        return None


def menuBebidas():
    print("=== Menú de Bebidas ===")
    bebidas = productos["bebidas"]
    for i, bebida in enumerate(bebidas):
        print(f"{i + 1}. {bebida['nombre']} - ${bebida['precio']}")

    opcion = input(f"Seleccione una bebida (1-{len(bebidas)}): ")

    try:
        index = int(opcion) - 1
        if 0 <= index < len(bebidas):
            item = bebidas[index]
            print(f"Ha seleccionado {item['nombre']}.")
            return (f"{item['nombre']} - ${item['precio']}", item['precio'])
        else:
            print("Opción inválida.")
            return None
    except ValueError:
        print("Opción inválida.")
        return None

def menuToppings():
    print("=== Menú de Adiciones ===")
    adiciones = productos["adiciones"]
    for i, adicion in enumerate(adiciones):
        print(f"{i + 1}. {adicion['nombre']} - ${adicion['precio']}")

    opcion = input(f"Seleccione una adición (1-{len(adiciones)}): ")

    try:
        index = int(opcion) - 1
        if 0 <= index < len(adiciones):
            item = adiciones[index]
            print(f"Ha seleccionado {item['nombre']}.")
            return (f"{item['nombre']} - ${item['precio']}", item['precio'])
        else:
            print("Opción inválida.")
            return None
    except ValueError:
        print("Opción inválida.")
        return None
