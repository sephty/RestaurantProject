from utils.fileHandler import load_json, save_json
from utils.path import CLIENT_FILE, PRODUCT_FILE
import os

productos = load_json(PRODUCT_FILE) or {"pizzas": [], "bebidas": [], "toppings": [], "salsas": []}
cliente_data = load_json(CLIENT_FILE) or {"clientes": []}

def limpiarPantalla():
    input("Presione Enter para continuar...")
    os.system('cls' if os.name == 'nt' else 'clear')
    
def menuPizzas():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== Menú de Pizzas ===")
    pizzas = productos["pizzas"]
    for i, pizza in enumerate(pizzas):
        print(f"{i + 1}. {pizza['nombre']} ({pizza['code']}) - ${pizza['precio']}")

    opcion = input(f"Seleccione una pizza (1-{len(pizzas)}): ")

    try:
        index = int(opcion) - 1
        if 0 <= index < len(pizzas):
            item = pizzas[index]
            nombre_pizza = item['nombre']
            precio_pizza = item['precio']
            code_pizza = item['code']

            print("¿Desea agregar toppings a esta pizza? (s/n): ")
            agregar_toppings = input().lower() == 's'

            toppings_seleccionados = []
            precio_total = precio_pizza
            toppings_codes = []

            if agregar_toppings:
                toppings = productos["toppings"]
                while True:
                    print("Toppings disponibles:")
                    for i, topping in enumerate(toppings):
                        print(f"{i + 1}. {topping['nombre']} ({topping['code']}) - ${topping['precio']}")

                    opcion_topping = input("Seleccione un topping (número) o 'fin' para terminar: ")
                    if opcion_topping.lower() == 'fin':
                        break

                    try:
                        index_topping = int(opcion_topping) - 1
                        if 0 <= index_topping < len(toppings):
                            topping = toppings[index_topping]
                            toppings_seleccionados.append(topping['nombre'])
                            toppings_codes.append(topping['code'])
                            precio_total += topping['precio']
                            print(f"Agregado: {topping['nombre']}")
                        else:
                            print("Opción inválida.")
                    except ValueError:
                        print("Opción inválida.")

            nombre_final = nombre_pizza
            if toppings_seleccionados:
                nombre_final += f" con {', '.join(toppings_seleccionados)}"

            print(f"Ha seleccionado {nombre_final}.")
            
            return (code_pizza, precio_total)  
        else:
            print("Opción inválida.")
            return None
    except ValueError:
        print("Opción inválida.")
        return None


def menuBebidas():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== Menú de Bebidas ===")
    bebidas = productos["bebidas"]
    for i, bebida in enumerate(bebidas):
        print(f"{i + 1}. {bebida['nombre']} ({bebida['code']}) - ${bebida['precio']}")

    opcion = input(f"Seleccione una bebida (1-{len(bebidas)}): ")

    try:
        index = int(opcion) - 1
        if 0 <= index < len(bebidas):
            item = bebidas[index]
            print(f"Ha seleccionado {item['nombre']}.")
            return (item['code'], item['precio'])
        else:
            print("Opción inválida.")
            return None
    except ValueError:
        print("Opción inválida.")
        return None

def menuSalsas():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== Menú de Salsas ===")
    salsas = productos["salsas"]
    for i, salsa in enumerate(salsas):
        print(f"{i + 1}. {salsa['nombre']} ({salsa['code']}) - ${salsa['precio']}")

    opcion = input(f"Seleccione una salsa (1-{len(salsas)}): ")

    try:
        index = int(opcion) - 1
        if 0 <= index < len(salsas):
            item = salsas[index]
            print(f"Ha seleccionado {item['nombre']}.")
            return (item['code'], item['precio'])
        else:
            print("Opción inválida.")
            return None
    except ValueError:
        print("Opción inválida.")
        return None
