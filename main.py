"""
Punto de entrada principal de la aplicación de gestión de pizzería.
Inicializa y ejecuta el menú principal que permite a los usuarios navegar por
las diferentes funcionalidades del sistema de pedidos y administración.
"""

from controllers.menuMain import menuPrincipal

if __name__ == "__main__":
    print("=== Bienvenido a la Pizzería ===")
    menuPrincipal()
