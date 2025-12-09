"""
Módulo de gestión del carrito de compras.
"""

from utils.productos import get_product_by_code

compras_global = {}
totalPagar_global = 0

def defCompras(compras):
    """Retorna una cadena con el detalle de las compras."""
    if not compras:
        return "Ninguna compra todavía"

    partes = []
    for code, datos in compras.items():
        cantidad = datos['cantidad']

        # Verificar si es una pizza personalizada (con toppings)
        if "_" in code and code.startswith("P"):
            # Descomponer el código personalizado
            parts = code.split("_")
            pizza_code = parts[0]
            toppings_codes = parts[1:]

            # Obtener la pizza base
            pizza = get_product_by_code(pizza_code)
            if pizza:
                pizza_nombre = pizza['nombre']

                # Agregar toppings si existen
                if toppings_codes:
                    toppings_nombres = []
                    for t_code in toppings_codes:
                        topping = get_product_by_code(t_code)
                        if topping:
                            toppings_nombres.append(topping['nombre'])

                    if toppings_nombres:
                        # Formato mejorado para toppings
                        if len(toppings_nombres) <= 3:
                            # Pocos toppings: mostrar todos en una línea clara
                            toppings_str = ", ".join(toppings_nombres)
                            partes.append(f"{pizza_nombre} [{toppings_str}] x{cantidad}")
                        else:
                            # Muchos toppings: mostrar primeros 2 + cantidad restante
                            primeros_dos = ", ".join(toppings_nombres[:2])
                            restantes = len(toppings_nombres) - 2
                            partes.append(f"{pizza_nombre} [{primeros_dos} +{restantes} más] x{cantidad}")
                    else:
                        partes.append(f"{pizza_nombre} x{cantidad}")
                else:
                    partes.append(f"{pizza_nombre} x{cantidad}")
            else:
                partes.append(f"{code} x{cantidad}")
        else:
            # Producto normal
            product = get_product_by_code(code)
            if product:
                nombre = product['nombre']
                partes.append(f"{nombre} x{cantidad}")
            else:
                partes.append(f"{code} x{cantidad}")

    # Unir con separador claro
    resultado = " | ".join(partes)

    # Si es muy largo, mostrar resumen
    if len(resultado) > 100:
        total_items = sum(datos['cantidad'] for datos in compras.values())
        tipos_unicos = len(compras)
        if tipos_unicos == 1:
            resultado = f"{total_items} unidad(es) - detalles arriba"
        else:
            resultado = f"{tipos_unicos} productos diferentes - detalles arriba"

    return resultado

def eliminarCompra():
    """Permite eliminar productos del carrito de compras."""
    global compras_global, totalPagar_global
    if not compras_global:
        print("No hay compras para eliminar.")
        return
    print("Compras actuales:")
    for code, datos in compras_global.items():
        product = get_product_by_code(code)
        nombre = product['nombre'] if product else code
        print(f"{code}: {nombre} (x{datos['cantidad']})")

    try:
        code = input("Ingrese el código del producto a eliminar: ").upper()
    except KeyboardInterrupt:
        print("\nOperación cancelada.")
        return

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
            except KeyboardInterrupt:
                print("\nOperación cancelada.")
                return

        compras_global[code]["cantidad"] -= cantidad_eliminar
        totalPagar_global -= precio_unit * cantidad_eliminar
        if compras_global[code]["cantidad"] == 0:
            del compras_global[code]
        print("Producto(s) eliminado(s) correctamente.")
    else:
        print("Producto no encontrado en compras.")

def agregarProductoCarrito(code, precio):
    """Agrega un producto al carrito de compras."""
    global compras_global, totalPagar_global

    if code in compras_global:
        compras_global[code]["cantidad"] += 1
    else:
        compras_global[code] = {"precio": precio, "cantidad": 1}

    totalPagar_global += precio

def obtenerCompras():
    """Retorna el estado actual del carrito."""
    return compras_global, totalPagar_global

def limpiarCarrito():
    """Limpia completamente el carrito de compras."""
    global compras_global, totalPagar_global
    compras_global = {}
    totalPagar_global = 0
