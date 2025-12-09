def menuBebidas():
    recargarProductos()
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== Menú de Bebidas - Pizzería ===")
    bebidas = productos["bebidas"]
    
    if not bebidas:
        print("No hay bebidas disponibles.")
        return None
    
    for i, bebida in enumerate(bebidas):
        print(f"{i + 1}. {bebida['nombre']} ({bebida['code']}) - ${bebida['precio']}")

    opcion = validar_entero_menu(f"Seleccione una bebida (1-{len(bebidas)}): ", 1, len(bebidas))
    if opcion is None:
        return None

    index = opcion - 1
    item = bebidas[index]
    print(f"✓ Ha seleccionado {item['nombre']}.")
    return (item['code'], item['precio'])