import os
from utils.fileHandler import load_json, save_json
from utils.menuApp import menuPizzas, menuBebidas, limpiarPantalla
from utils.path import CLIENT_FILE, PRODUCT_FILE

usuario_actual = None
compras_global = {}
totalPagar_global = 0

productos = load_json(PRODUCT_FILE) or {"pizzas": [], "bebidas": [], "toppings": [], "salsas": []}
cliente_data = load_json(CLIENT_FILE) or {"clientes": []}
    



def eliminarCompra():
    global compras_global, totalPagar_global
    if not compras_global:
        print("No hay compras para eliminar.")
        return
    print("Compras actuales:")
    for code, datos in compras_global.items():
        product = get_product_by_code(code)
        nombre = product['nombre'] if product else code
        print(f"{code}: {nombre} (x{datos['cantidad']})")
    code = input("Ingrese el código del producto a eliminar: ").upper()
    if code in compras_global:
        cantidad_actual = compras_global[code]["cantidad"]
        precio_unit = compras_global[code]["precio"]
        if cantidad_actual == 1:
            cantidad_eliminar = 1
        else:
            try:
                cantidad_eliminar = int(input(f"Cuántos {get_product_by_code(code)['nombre'] if get_product_by_code(code) else code} desea eliminar (1-{cantidad_actual}): "))
                if cantidad_eliminar < 1 or cantidad_eliminar > cantidad_actual:
                    print("Cantidad inválida.")
                    return
            except ValueError:
                print("Cantidad inválida.")
                return
        compras_global[code]["cantidad"] -= cantidad_eliminar
        totalPagar_global -= precio_unit * cantidad_eliminar
        if compras_global[code]["cantidad"] == 0:
            del compras_global[code]
        print("Producto(s) eliminado(s) correctamente.")
    else:
        print("Producto no encontrado en compras.")
    
def defCompras(compras):
    if not compras:
        return "Ninguna compra todavía"
    
    partes = []
    for code, datos in compras.items():
        product = get_product_by_code(code)
        if product:
            nombre = product['nombre']
            partes.append(f"{nombre} (x{datos['cantidad']})")
        else:
            partes.append(f"{code} (x{datos['cantidad']})")
    return ", ".join(partes)

def cargarPedido():
    global usuario_actual, compras_global, totalPagar_global
    nombre = input("Ingrese el nombre del cliente para cargar: ")
    for cliente in cliente_data["clientes"]:
        if cliente["nombre"].lower() == nombre.lower():
            usuario_actual = cliente
            compras_global = {}
            totalPagar_global = 0
            for code in cliente["pedidos"]:
                product = get_product_by_code(code)
                if product:
                    precio = product['precio']
                    if code in compras_global:
                        compras_global[code]["cantidad"] += 1
                    else:
                        compras_global[code] = {"precio": precio, "cantidad": 1}
                    totalPagar_global += precio
            print("Cliente cargado.")
            return True
    print("Cliente no encontrado.")
    return False

def guardarPedido(compras):
    global usuario_actual
    if not compras:
        print("No hay compras para guardar.")
        return
    if usuario_actual is None:
        nombre_cliente = input("Ingrese el nombre del cliente: ")
    else:
        nombre_cliente = usuario_actual["nombre"]
    pedidos = []
    for code, datos in compras.items():
        for _ in range(datos['cantidad']):
            pedidos.append(code)
    if usuario_actual:
        usuario_actual["pedidos"] = pedidos
        for i, cli in enumerate(cliente_data["clientes"]):
            if cli["nombre"] == nombre_cliente:
                cliente_data["clientes"][i] = usuario_actual
                print("Pedido guardado correctamente.")
                break
    else:
        new_id = len(cliente_data["clientes"]) + 1
        new_cliente = {"id": new_id, "nombre": nombre_cliente, "pedidos": pedidos}
        cliente_data["clientes"].append(new_cliente)
        usuario_actual = new_cliente
        print("Pedido guardado correctamente.")
    save_json(CLIENT_FILE, cliente_data)

def menuGestionProductos():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== Gestión de Productos ===")
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
        limpiarPantalla()

def modifyProducto():
    tipo = input("Ingrese el tipo de producto (pizza, bebida o topping): ").lower()
    if tipo not in ["pizza", "bebida", "topping"]:
        print("Tipo inválido.")
        return
    print("Productos disponibles:")
    categoria = productos[tipo + "s"]
    for item in categoria:
        print(f"{item['code']}: {item['nombre']} - ${item['precio']}")
    code = input("Ingrese el código del producto a modificar: ").upper()
    for i, item in enumerate(categoria):
        if item['code'] == code:
            nuevo_nombre = input(f"Nuevo nombre ({item['nombre']}): ") or item['nombre']
            nuevo_precio = input(f"Nuevo precio ({item['precio']}): ")
            try:
                nuevo_precio = int(nuevo_precio) if nuevo_precio else item['precio']
            except ValueError:
                print("Precio inválido.")
                return
            categoria[i]['nombre'] = nuevo_nombre
            categoria[i]['precio'] = nuevo_precio
            save_json(PRODUCT_FILE, productos)
            print("Producto modificado correctamente.")
            return
    print("Producto no encontrado.")

def deleteProducto():
    tipo = input("Ingrese el tipo de producto (pizza, bebida o topping): ").lower()
    if tipo not in ["pizza", "bebida", "topping"]:
        print("Tipo inválido.")
        return
    print("Productos disponibles:")
    categoria = productos[tipo + "s"]
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
        
def get_next_code(tipo):
    if tipo == "pizza":
        existing = [p["code"] for p in productos["pizzas"]]
        prefix = "P"
    elif tipo == "bebida":
        existing = [b["code"] for b in productos["bebidas"]]
        prefix = "B"
    elif tipo == "topping":
        existing = [t["code"] for t in productos["toppings"]]
        prefix = "T"
    else:
        return None
    numbers = [int(code[1:]) for code in existing if code.startswith(prefix) and code[1:].isdigit()]
    next_num = max(numbers) + 1 if numbers else 1
    return f"{prefix}{next_num:03d}"

def get_product_by_code(code):
    for categoria in productos.values():
        for item in categoria:
            if item["code"] == code:
                return item
    return None

def addProducto():
    tipo = input("Ingrese el tipo de producto (pizza, bebida o topping): ").lower()
    nombre = input("Ingrese el nombre del producto: ")
    precio = int(input("Ingrese el precio del producto: "))
    code = get_next_code(tipo)
    if code is None:
        print("Tipo de producto inválido.")
        return
    new_product = {"code": code, "nombre": nombre, "precio": precio}
    if tipo == "pizza":
        productos["pizzas"].append(new_product)
    elif tipo == "bebida":
        productos["bebidas"].append(new_product)
    elif tipo == "topping":
        productos["toppings"].append(new_product)
    save_json(PRODUCT_FILE, productos)
    print(f"Producto agregado correctamente con código: {code}.")
    

def menuPrincipal():
    global compras_global, totalPagar_global
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== Menú Principal ===")
        print("1. Pizzas")
        print("2. Bebidas")
        print("3. Toppings")
        print("4. Guardar Pedido")
        print("5. Cargar Pedido")
        print("6. Eliminar Compra")
        print("7. Gestionar Productos")
        print("0. Salir")
        usuario_display = usuario_actual["nombre"] if usuario_actual else "Ninguno"
        print(f" Usuario actual: {usuario_display}")

        print(f"「El total a pagar es: ${totalPagar_global}")
        print(f"  Detalles de la compra: {defCompras(compras_global)} 」")

        opcion = input("Seleccione una opción (0-5): ")
        resultado = None
    
        match opcion:
            case '1':
                resultado = menuPizzas()
            case '2':
                resultado = menuBebidas()
            case '3':
                print ("abc")
                return
            case '4':
                guardarPedido(compras_global)
            case '5':
                cargarPedido()
            case '6':
                eliminarCompra()
            case '7':
                menuGestionProductos()
            case '0':
                print("Gracias por su compra. ¡Hasta luego!")
                break
            case _:
                print("Opción inválida.")
                continue
            
        if resultado:
            code, precio = resultado

            if code in compras_global:
                compras_global[code]["cantidad"] += 1
            else:
                compras_global[code] = {"precio": precio, "cantidad": 1}

            totalPagar_global += precio

        limpiarPantalla()

menuPrincipal()
