"""
Módulo de utilidades para gestión de productos.
"""

from utils.fileHandler import load_json
from utils.path import PRODUCT_FILE

productos = load_json(PRODUCT_FILE) or {"pizzas": [], "bebidas": [], "toppings": [], "adiciones": [], "salsas": []}

def recargarProductos():
    """Recarga los productos desde el archivo JSON."""
    global productos
    productos = load_json(PRODUCT_FILE) or {"pizzas": [], "bebidas": [], "toppings": [], "adiciones": [], "salsas": []}

def get_product_by_code(code):
    """Obtiene un producto por su código."""
    recargarProductos()
    for categoria in productos.values():
        for item in categoria:
            if item["code"] == code:
                return item
    return None

def get_next_code(tipo):
    """Genera el siguiente código disponible para un tipo de producto."""
    recargarProductos()
    if tipo == "pizza":
        existing = [p["code"] for p in productos["pizzas"]]
        prefix = "P"
    elif tipo == "bebida":
        existing = [b["code"] for b in productos["bebidas"]]
        prefix = "B"
    elif tipo == "adicion":
        existing = [a["code"] for a in productos["adiciones"]]
        prefix = "A"
    elif tipo == "topping":
        existing = [t["code"] for t in productos["toppings"]]
        prefix = "T"
    elif tipo == "salsa":
        existing = [s["code"] for s in productos["salsas"]]
        prefix = "S"
    else:
        return None
    numbers = [int(code[1:]) for code in existing if code.startswith(prefix) and code[1:].isdigit()]
    next_num = max(numbers) + 1 if numbers else 1
    return f"{prefix}{next_num:03d}"

def obtenerProductos():
    """Retorna la estructura completa de productos."""
    recargarProductos()
    return productos
