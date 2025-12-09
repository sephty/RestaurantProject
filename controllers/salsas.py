def menuSalsas():
    recargarProductos()
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== Menú de Salsas - Pizzería ===")
    salsas = productos["salsas"]
    
    if not salsas:
        print("No hay salsas disponibles.")
        return None
    
    for i, salsa in enumerate(salsas):
        print(f"{i + 1}. {salsa['nombre']} ({salsa['code']}) - ${salsa['precio']}")

    opcion = validar_entero_menu(f"Seleccione una salsa (1-{len(salsas)}): ", 1, len(salsas))
    if opcion is None:
        return None

    index = opcion - 1
    item = salsas[index]
    print(f"✓ Ha seleccionado {item['nombre']}.")
    return (item['code'], item['precio'])