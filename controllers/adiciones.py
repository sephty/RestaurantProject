def menuAdiciones():
    recargarProductos()
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== Menú de Adiciones - Pizzería ===")
    adiciones = productos["adiciones"]

    if not adiciones:
        print("No hay adiciones disponibles.")
        return None

    for i, adicion in enumerate(adiciones):
        print(f"{i + 1}. {adicion['nombre']} ({adicion['code']}) - ${adicion['precio']}")

    opcion = validar_entero_menu(f"Seleccione una adición (1-{len(adiciones)}): ", 1, len(adiciones))
    if opcion is None:
        return None

    index = opcion - 1
    item = adiciones[index]
    print(f"✓ Ha seleccionado {item['nombre']}.")
    return (item['code'], item['precio'])