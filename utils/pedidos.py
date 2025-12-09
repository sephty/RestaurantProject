"""
Módulo responsable de la gestión completa de pedidos de clientes.
Permite guardar pedidos en el perfil del cliente actual y cargar pedidos
previos desde archivos JSON, facilitando la persistencia de órdenes
y la recuperación de historiales de compra.
"""

from utils.fileHandler import load_json, save_json
from utils.path import CLIENT_FILE
from utils.productos import get_product_by_code
from utils.autenticacion import obtenerUsuarioActual, usuario_actual

cliente_data = load_json(CLIENT_FILE) or {"clientes": []}

def recargarClientes():
    """Recarga los datos de clientes desde el archivo JSON."""
    global cliente_data
    cliente_data = load_json(CLIENT_FILE) or {"clientes": []}

def cargarPedido():
    """Carga y restaura el pedido guardado de un cliente existente desde el archivo de clientes.
    Permite buscar por nombre y reconstruye el carrito de compras con los productos previos,
    incluyendo manejo especial para pizzas personalizadas con toppings."""
    import utils.comprasMan
    from utils.autenticacion import esAdmin
    recargarClientes()

    nombre = input("Ingrese el nombre del cliente para cargar: ")
    for cliente in cliente_data["clientes"]:
        if cliente["nombre"].lower() == nombre.lower():
            # Set the user as current user (directly modify the imported variable)
            import utils.autenticacion
            utils.autenticacion.usuario_actual = cliente

            # Clear current cart and load client's orders
            utils.comprasMan.limpiarCarrito()

            for code in cliente["pedidos"]:
                # Handle custom pizza codes (P001_T001 format)
                if "_" in code and code.startswith("P"):
                    # Extract base pizza code
                    base_code = code.split("_")[0]
                    base_product = get_product_by_code(base_code)
                    if base_product:
                        # Calculate total price (base pizza + toppings)
                        precio_total = base_product['precio']
                        topping_codes = code.split("_")[1:]
                        for t_code in topping_codes:
                            topping = get_product_by_code(t_code)
                            if topping:
                                precio_total += topping['precio']
                        utils.comprasMan.agregarProductoCarrito(code, precio_total)
                else:
                    # Regular product
                    product = get_product_by_code(code)
                    if product:
                        precio = product['precio']
                        utils.comprasMan.agregarProductoCarrito(code, precio)

            print(f"Cliente cargado: {cliente['nombre']}")
            if esAdmin():
                print("(Cuenta de administrador)")
            return True
    print("Cliente no encontrado.")
    return False

def guardarPedido(compras):
    """Guarda el pedido actual del cliente en su perfil, actualizando o creando el registro del cliente.
    Convierte los productos del carrito en una lista de códigos y los almacena en el archivo de clientes JSON."""
    recargarClientes()

    if not compras:
        print("No hay compras para guardar.")
        return

    usuario_actual = obtenerUsuarioActual()
    if usuario_actual is None:
        nombre_cliente = input("Ingrese el nombre del cliente: ")
        # Verificar si existe
        for cliente in cliente_data["clientes"]:
            if cliente["nombre"].lower() == nombre_cliente.lower():
                usuario_actual = cliente
                break
    else:
        nombre_cliente = usuario_actual["nombre"]

    pedidos = []
    for code, datos in compras.items():
        for _ in range(datos['cantidad']):
            pedidos.append(code)

    if usuario_actual:
        usuario_actual["pedidos"] = pedidos
        for i, cli in enumerate(cliente_data["clientes"]):
            if cli["nombre"].lower() == nombre_cliente.lower():
                cliente_data["clientes"][i] = usuario_actual
                # Set as current user
                import utils.autenticacion
                utils.autenticacion.usuario_actual = usuario_actual
                print("Pedido guardado correctamente.")
                break
    else:
        new_id = len(cliente_data["clientes"]) + 1
        new_cliente = {
            "id": new_id,
            "nombre": nombre_cliente,
            "admin": False,
            "pedidos": pedidos
        }
        cliente_data["clientes"].append(new_cliente)
        # Set as current user
        import utils.autenticacion
        utils.autenticacion.usuario_actual = new_cliente
        print("Pedido guardado correctamente.")

    save_json(CLIENT_FILE, cliente_data)
