"""
Controlador principal que gestiona la interfaz de usuario del sistema de pizzería.
Coordina la navegación entre diferentes menús (pizzas, bebidas, adiciones, salsas),
maneja las operaciones del carrito de compras y proporciona acceso a funciones
de administración para usuarios con permisos especiales.
"""

import os
from utils.autenticacion import obtenerUsuarioActual, esAdmin
from utils.comprasMan import defCompras, obtenerCompras, eliminarCompra, agregarProductoCarrito
from utils.pedidos import guardarPedido, cargarPedido
from utils.menuApp import menuPizzas, menuBebidas, menuAdiciones, menuSalsas, limpiarPantalla
from controllers.admin import menuGestionProductos

def menuPrincipal():
    """Ejecuta el bucle principal del menú de la pizzería, mostrando opciones para
    seleccionar productos, gestionar pedidos, administrar productos (para admins)
    y manejar operaciones del carrito de compras en un ciclo continuo hasta salir."""
    compras_global, totalPagar_global = obtenerCompras()

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== Menú Principal - Pizzería ===")
        print("1. Pizzas")
        print("2. Bebidas")
        print("3. Adiciones")
        print("4. Salsas")
        print("5. Guardar Pedido")
        print("6. Cargar Pedido")
        print("7. Eliminar Compra")
        if esAdmin():
            print("8. Gestionar Productos (Admin)")
        print("0. Salir")

        usuario_display = obtenerUsuarioActual()["nombre"] if obtenerUsuarioActual() else "Ninguno"
        admin_status = " (Admin)" if esAdmin() else ""
        print(f"\n Usuario actual: {usuario_display}{admin_status}")
        print(f" Total a pagar: ${totalPagar_global}")
        print(f" Pedido actual: {defCompras(compras_global)}")

        try:
            opcion = input("\nSeleccione una opción: ")
        except KeyboardInterrupt:
            print("\n\nGracias por su compra. ¡Hasta luego!")
            break

        resultado = None

        try:
            match opcion:
                case '1':
                    resultado = menuPizzas()
                case '2':
                    resultado = menuBebidas()
                case '3':
                    resultado = menuAdiciones()
                case '4':
                    resultado = menuSalsas()
                case '5':
                    guardarPedido(compras_global)
                case '6':
                    if cargarPedido():
                        compras_global, totalPagar_global = obtenerCompras()
                case '7':
                    eliminarCompra()
                    # Update local variables after removing from cart
                    compras_global, totalPagar_global = obtenerCompras()
                case '8':
                    if esAdmin():
                        menuGestionProductos()
                    else:
                        print("Opción inválida o no tiene permisos.")
                case '0':
                    print("Gracias por su compra. ¡Hasta luego!")
                    break
                case _:
                    print("Opción inválida.")
                    continue

        except Exception as e:
            print(f"Error inesperado al procesar la opción {opcion}: {e}")
            continue

        if resultado:
            code, precio = resultado
            agregarProductoCarrito(code, precio)
            # Update local variables after adding to cart
            compras_global, totalPagar_global = obtenerCompras()

        limpiarPantalla()
