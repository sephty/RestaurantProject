def menuPizzas():
    recargarProductos()
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== Menú de Pizzas - Pizzería ===")
    pizzas = productos["pizzas"]
    
    if not pizzas:
        print("No hay pizzas disponibles.")
        return None
    
    for i, pizza in enumerate(pizzas):
        print(f"{i + 1}. {pizza['nombre']} ({pizza['code']}) - ${pizza['precio']}")

    opcion = validar_entero_menu(f"Seleccione una pizza (1-{len(pizzas)}): ", 1, len(pizzas))
    if opcion is None:
        return None

    index = opcion - 1
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
            print("\nToppings disponibles:")
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
                    print(f"✓ Agregado: {topping['nombre']}")
                else:
                    print("Opción inválida.")
            except ValueError:
                print("Opción inválida.")

    nombre_final = nombre_pizza
    if toppings_seleccionados:
        nombre_final += f" con {', '.join(toppings_seleccionados)}"

    print(f"\n✓ Ha seleccionado {nombre_final}.")

    # Devolver código especial que incluye toppings si los hay
    if toppings_seleccionados:
        # Crear un código único para esta pizza personalizada
        toppings_str = "_".join(toppings_codes)
        code_custom = f"{code_pizza}_{toppings_str}"
        return (code_custom, precio_total)
    else:
        return (code_pizza, precio_total)

def menuToppings():
    recargarProductos()
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== Menú de Toppings (Adiciones) - Pizzería ===")
    toppings = productos["toppings"]
    
    if not toppings:
        print("No hay toppings disponibles.")
        return None
    
    for i, topping in enumerate(toppings):
        print(f"{i + 1}. {topping['nombre']} ({topping['code']}) - ${topping['precio']}")

    opcion = validar_entero_menu(f"Seleccione un topping (1-{len(toppings)}): ", 1, len(toppings))
    if opcion is None:
        return None

    index = opcion - 1
    item = toppings[index]
    print(f"✓ Ha seleccionado {item['nombre']}.")
    return (item['code'], item['precio'])