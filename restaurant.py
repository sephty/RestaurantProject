import os
from utils.fileHandler import load_json, save_json

usuario_actual = None
compras_global = {}
totalPagar_global = 0

productos = load_json("productos.json") or {"platillos": [], "bebidas": [], "adiciones": []}
cliente_data = load_json("cliente.json") or {"clientes": []}
    
CLIENT_FILE = open("cliente.json")
PRODUCT_FILE = open("productos.json")

def limpiarPantalla():
    input("Presione Enter para continuar...")
    os.system('cls' if os.name == 'nt' else 'clear')

def menuPlatillos():
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

def menuAdiciones():
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
    
def eliminarProducto():
    global compras_global, totalPagar_global
    producto = input("Ingrese el nombre del producto a eliminar: ")
    if producto in compras_global:
        totalPagar_Global -= compras_global[producto]["precio"]
        del compras_global[producto]
        print("Producto eliminado correctamente.")
    
def defCompras(compras):
    if not compras:
        return "Ninguna compra todavía"
    
    partes = []
    for item, datos in compras.items():
        partes.append(f"{item} (x{datos['cantidad']})")
    return ", ".join(partes)

def cargarPedido():
    global usuario_actual, compras_global, totalPagar_global
    nombre = input("Ingrese el nombre del cliente para cargar: ")
    for cliente in cliente_data["clientes"]:
        if cliente["nombre"].lower() == nombre.lower():
            usuario_actual = cliente
            compras_global = {}
            totalPagar_global = 0
            for pedido in cliente["pedidos"]:
                precio = None
                for categoria in productos.values():
                    for item in categoria:
                        if f"{item['nombre']} - ${item['precio']}" == pedido:
                            precio = item['precio']
                            break
                    if precio is not None:
                        break
                if precio is not None:
                    if pedido in compras_global:
                        compras_global[pedido]["cantidad"] += 1
                    else:
                        compras_global[pedido] = {"precio": precio, "cantidad": 1}
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
    for item, datos in compras.items():
        for _ in range(datos['cantidad']):
            pedidos.append(item)
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
    save_json("cliente.json", cliente_data)
        
def addProducto():
    tipo = input("Ingrese el tipo de producto (platillo, bebida o adicion): ")
    nombre = input("Ingrese el nombre del producto: ")
    precio = int(input("Ingrese el precio del producto: "))
    if tipo == "platillo":
        productos["platillos"].append({"nombre": nombre, "precio": precio})
    elif tipo == "bebida":
        productos["bebidas"].append({"nombre": nombre, "precio": precio})
    elif tipo == "adicion":
        productos["adiciones"].append({"nombre": nombre, "precio": precio})
    else:
        print("Tipo de producto inválido.")
    save_json("productos.json", productos)
    print("Producto agregado correctamente.")
    

def menuPrincipal():
    global compras_global, totalPagar_global
    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        print("=== Menú Principal ===")
        print("1. Platillos")
        print("2. Bebidas")
        print("3. Adiciones")
        print("4. Guardar Pedido")
        print("5. Cargar Pedido")
        print("6. Agregar Producto")
        print("7. Eliminar Producto")
        print("0. Salir")
        usuario_display = usuario_actual["nombre"] if usuario_actual else "Ninguno"
        print(f" Usuario actual: {usuario_display}")
        print(f"「El total a pagar es: ${totalPagar_global}")
        print(f"  Detalles de la compra: {defCompras(compras_global)} 」")

        opcion = input("Seleccione una opción (0-5): ")
        resultado = None
    
        match opcion:
            case '1':
                resultado = menuPlatillos()
            case '2':
                resultado = menuBebidas()
            case '3':
                resultado = menuAdiciones()
            case '4':
                guardarPedido(compras_global)
            case '5':
                cargarPedido()
            case '6':
                addProducto()
            case '7':
                eliminarProducto()
            case '0':
                print("Gracias por su compra. ¡Hasta luego!")
                break
            case _:
                print("Opción inválida.")
                continue
            
        if resultado:
            nombre, precio = resultado

            if nombre in compras_global:
                compras_global[nombre]["cantidad"] += 1
            else:
                compras_global[nombre] = {"precio": precio, "cantidad": 1}

            totalPagar_global += precio

        limpiarPantalla()

menuPrincipal()
