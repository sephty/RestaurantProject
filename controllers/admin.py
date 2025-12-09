"""
Controlador de administración - gestión de productos.
"""

import os
from utils.fileHandler import save_json
from utils.path import PRODUCT_FILE
from utils.productos import get_next_code, obtenerProductos, recargarProductos

productos = obtenerProductos()

def addProducto():
    """Agrega un nuevo producto al sistema."""
    global productos
    recargarProductos()

    print("Tipos disponibles: pizza, bebida, adicion, topping, salsa")
    tipo = input("Ingrese el tipo de producto: ").lower().strip()

    if tipo not in ["pizza", "bebida", "adicion", "topping", "salsa"]:
        print("Tipo de producto inválido.")
        return

    nombre = input("Ingrese el nombre del producto: ").strip()
    if not nombre:
        print("Error: El nombre del producto no puede estar vacío.")
        return

    try:
        precio = int(input("Ingrese el precio del producto: "))
        if precio < 0:
            print("Error: El precio no puede ser negativo.")
            return
    except ValueError:
        print("Error: Precio inválido.")
        return

    code = get_next_code(tipo)
    if code is None:
        print("Error al generar código.")
        return

    new_product = {"code": code, "nombre": nombre, "precio": precio}

    if tipo == "pizza":
        productos["pizzas"].append(new_product)
    elif tipo == "bebida":
        productos["bebidas"].append(new_product)
    elif tipo == "adicion":
        productos["adiciones"].append(new_product)
    elif tipo == "topping":
        productos["toppings"].append(new_product)
    elif tipo == "salsa":
        productos["salsas"].append(new_product)

    save_json(PRODUCT_FILE, productos)
    print(f"Producto agregado correctamente con código: {code}.")

def modifyProducto():
    """Modifica un producto existente."""
    global productos
    recargarProductos()

    print("Tipos disponibles: pizza, bebida, adicion, topping, salsa")
    tipo = input("Ingrese el tipo de producto: ").lower()

    if tipo not in ["pizza", "bebida", "adicion", "topping", "salsa"]:
        print("Tipo inválido.")
        return

    categoria_nombre = tipo + "s"
    if tipo == "salsa":
        categoria_nombre = "salsas"

    print("Productos disponibles:")
    categoria = productos[categoria_nombre]

    if not categoria:
        print("No hay productos en esta categoría.")
        return

    for item in categoria:
        print(f"{item['code']}: {item['nombre']} - ${item['precio']}")

    code = input("Ingrese el código del producto a modificar: ").upper()
    for i, item in enumerate(categoria):
        if item['code'] == code:
            nuevo_nombre = input(f"Nuevo nombre ({item['nombre']}): ") or item['nombre']
            try:
                nuevo_precio_str = input(f"Nuevo precio ({item['precio']}): ")
                nuevo_precio = int(nuevo_precio_str) if nuevo_precio_str else item['precio']
                if nuevo_precio < 0:
                    print("Error: El precio no puede ser negativo.")
                    return
            except ValueError:
                print("Error: Precio inválido.")
                return

            categoria[i]['nombre'] = nuevo_nombre
            categoria[i]['precio'] = nuevo_precio
            save_json(PRODUCT_FILE, productos)
            print("Producto modificado correctamente.")
            return
    print("Producto no encontrado.")

def deleteProducto():
    """Elimina un producto del sistema."""
    global productos
    recargarProductos()

    print("Tipos disponibles: pizza, bebida, adicion, topping, salsa")
    tipo = input("Ingrese el tipo de producto: ").lower()

    if tipo not in ["pizza", "bebida", "adicion", "topping", "salsa"]:
        print("Tipo inválido.")
        return

    categoria_nombre = tipo + "s"
    if tipo == "salsa":
        categoria_nombre = "salsas"

    print("Productos disponibles:")
    categoria = productos[categoria_nombre]

    if not categoria:
        print("No hay productos en esta categoría.")
        return

    for item in categoria:
        print(f"{item['code']}: {item['nombre']} - ${item['precio']}")

    code = input("Ingrese el código del producto a eliminar: ").upper()
    for i, item in enumerate(categoria):
        if item['code'] == code:
            confirm = input(f"¿Está seguro de eliminar {item['nombre']}? (s/n): ").lower()
            if confirm == 's':
                categoria.pop(i)
                save_json(PRODUCT_FILE, productos)
                print("Producto eliminado correctamente.")
            return
    print("Producto no encontrado.")

def menuGestionProductos():
    """Menú de gestión de productos (solo para administradores)."""
    from utils.autenticacion import esAdmin
    if not esAdmin():
        print("Acceso denegado. Solo los administradores pueden gestionar productos.")
        return

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== Gestión de Productos (Admin) - Pizzería ===")
        print("1. Agregar Producto")
        print("2. Modificar Producto")
        print("3. Eliminar Producto")
        print("0. Volver al Menú Principal")
        opcion = input("Seleccione una opción: ")
        if opcion == '1':
            addProducto()
        elif opcion == '2':
            modifyProducto()
        elif opcion == '3':
            deleteProducto()
        elif opcion == '0':
            break
        else:
            print("Opción inválida.")

        from utils.menuApp import limpiarPantalla
        limpiarPantalla()
