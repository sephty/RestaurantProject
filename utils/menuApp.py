"""
Generic menu utilities for product selection.
"""

from utils.productos import obtenerProductos
import os

def limpiarPantalla():
    """Clear screen utility."""
    try:
        input("Presione Enter para continuar...")
    except KeyboardInterrupt:
        print("\nOperación cancelada.")
    finally:
        os.system('cls' if os.name == 'nt' else 'clear')

def menu_selector(categoria, titulo, permitir_toppings=False):

    productos = obtenerProductos()

    if categoria not in productos:
        print(f"Error: Categoría '{categoria}' no encontrada.")
        return None

    items = productos[categoria]
    if not items:
        print(f"No hay {categoria} disponibles.")
        return None

    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"=== {titulo} - Pizzería ===")

    for i, item in enumerate(items):
        print(f"{i + 1}. {item['nombre']} ({item['code']}) - ${item['precio']}")

    while True:
        try:
            opcion = int(input(f"Seleccione una opción (1-{len(items)}): "))
            if 1 <= opcion <= len(items):
                break
            print("Opción inválida.")
        except ValueError:
            print("Por favor ingrese un número válido.")
        except KeyboardInterrupt:
            print("\nOperación cancelada.")
            return None

    if opcion is None:
        return None

    index = opcion - 1
    item = items[index]
    precio_total = item['precio']

    # Special handling for pizzas with toppings
    if permitir_toppings and categoria == 'pizzas':
        toppings = productos.get('toppings', [])
        if toppings:
            try:
                print("¿Desea agregar toppings? (s/n): ", end="")
                respuesta = input().lower()
                if respuesta == 's':
                    print("\nToppings disponibles:")
                    for i, topping in enumerate(toppings):
                        print(f"{i + 1}. {topping['nombre']} - ${topping['precio']}")

                    while True:
                        try:
                            topping_opcion = input("Seleccione topping (número) o 'fin': ")
                            if topping_opcion.lower() == 'fin':
                                break
                            topping_idx = int(topping_opcion) - 1
                            if 0 <= topping_idx < len(toppings):
                                topping = toppings[topping_idx]
                                precio_total += topping['precio']
                                print(f"✓ Agregado: {topping['nombre']}")
                            else:
                                print("Opción inválida.")
                        except ValueError:
                            print("Opción inválida.")
                        except KeyboardInterrupt:
                            print("\nOperación cancelada.")
                            return None
            except KeyboardInterrupt:
                print("\nOperación cancelada.")
                return None

    print(f"✓ Seleccionado: {item['nombre']}")
    return (item['code'], precio_total)

# Specific menu functions using the generic selector
def menuPizzas():
    return menu_selector('pizzas', 'Menú de Pizzas', permitir_toppings=True)

def menuBebidas():
    return menu_selector('bebidas', 'Menú de Bebidas')

def menuAdiciones():
    return menu_selector('adiciones', 'Menú de Adiciones')

def menuSalsas():
    return menu_selector('salsas', 'Menú de Salsas')
