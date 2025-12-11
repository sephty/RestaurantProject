
from utils.fileHandler import load_json

PRODUCT_FILE = "productos.json"
CLIENT_FILE = "cliente.json"

productos = load_json(PRODUCT_FILE) or {"pizzas": [], "bebidas": [], "toppings": [], "salsas": []}
cliente_data = load_json(CLIENT_FILE) or {"clientes": []}
