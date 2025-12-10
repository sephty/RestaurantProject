# Sistema de Gestión de Pizzería

## Resumen Ejecutivo

Este proyecto presenta un sistema integral de gestión para pizzerías desarrollado en Python, diseñado para facilitar la administración de productos, gestión de pedidos y autenticación de usuarios. El sistema implementa una arquitectura modular basada en el patrón Modelo-Vista-Controlador (MVC), utilizando persistencia de datos mediante archivos JSON y proporcionando una interfaz de usuario interactiva por consola.

## Descripción del Proyecto

### Contexto y Justificación

El Sistema de Gestión de Pizzería surge como respuesta a la necesidad de automatizar y optimizar los procesos operativos en establecimientos de comida rápida, específicamente pizzerías. El sistema permite gestionar eficientemente el catálogo de productos, procesar pedidos de clientes y administrar el inventario mediante una interfaz intuitiva de línea de comandos.

### Objetivos

#### Objetivo General
Desarrollar un sistema informático robusto y escalable para la gestión integral de operaciones en una pizzería, incluyendo la administración de productos, procesamiento de pedidos y control de acceso mediante autenticación de usuarios.

#### Objetivos Específicos
1. Implementar un módulo de autenticación que distinga entre usuarios regulares y administradores
2. Diseñar un sistema de gestión de productos que soporte múltiples categorías (pizzas, bebidas, adiciones, salsas)
3. Desarrollar un carrito de compras funcional con capacidad de persistencia de datos
4. Crear funcionalidades CRUD (Crear, Leer, Actualizar, Eliminar) para la administración de productos
5. Garantizar la persistencia de datos mediante el uso de archivos JSON
6. Proporcionar una interfaz de usuario clara y navegable por consola

## Arquitectura del Sistema

### Estructura del Proyecto

El proyecto sigue una arquitectura modular organizada en tres componentes principales:

```
RestaurantProject/
├── main.py                     # Punto de entrada de la aplicación
├── cliente.json                # Base de datos de usuarios
├── productos.json              # Base de datos de productos
├── controllers/                # Capa de controladores
│   ├── menuMain.py            # Controlador principal del menú
│   ├── admin.py               # Controlador de administración
│   ├── pizzas.py              # Controlador de pizzas
│   ├── bebidas.py             # Controlador de bebidas
│   ├── adiciones.py           # Controlador de adiciones
│   └── salsas.py              # Controlador de salsas
└── utils/                      # Capa de utilidades y lógica de negocio
    ├── autenticacion.py       # Módulo de autenticación
    ├── productos.py           # Gestión del catálogo de productos
    ├── comprasMan.py          # Gestión del carrito de compras
    ├── pedidos.py             # Gestión de pedidos
    ├── menuApp.py             # Utilidades de interfaz de menús
    ├── fileHandler.py         # Manejo de archivos JSON
    └── path.py                # Gestión de rutas de archivos
```

### Patrones de Diseño Implementados

#### 1. Modelo-Vista-Controlador (MVC)
- **Modelo**: Representado por los archivos JSON (`cliente.json`, `productos.json`) y los módulos de acceso a datos
- **Vista**: Implementada mediante las funciones de interfaz de usuario en consola
- **Controlador**: Módulos en el directorio `controllers/` que coordinan la lógica de negocio

#### 2. Separación de Responsabilidades
- **Controllers**: Gestionan la interacción con el usuario y la navegación entre menús
- **Utils**: Contienen la lógica de negocio y operaciones sobre datos
- **Data Layer**: Archivos JSON que actúan como base de datos persistente

## Funcionalidades Principales

### 1. Sistema de Autenticación

El módulo `autenticacion.py` proporciona:

- **Inicio de sesión**: Autenticación de usuarios existentes
- **Registro de usuarios**: Creación de nuevas cuentas de cliente
- **Modo invitado**: Navegación sin cuenta de usuario
- **Control de permisos**: Distinción entre usuarios regulares y administradores
- **Gestión de sesiones**: Mantenimiento del estado de usuario actual

```python
# Ejemplo de verificación de permisos
if esAdmin():
    # Acceso a funcionalidades administrativas
```

### 2. Gestión de Productos

El sistema maneja cinco categorías de productos:

- **Pizzas** (código P001, P002, ...)
- **Bebidas** (código B001, B002, ...)
- **Adiciones** (código A001, A002, ...)
- **Salsas** (código S001, S002, ...)
- **Toppings** (código T001, T002, ...)

#### Funcionalidades para Administradores
- Agregar nuevos productos con generación automática de códigos únicos
- Modificar productos existentes (nombre y precio)
- Eliminar productos del catálogo
- Validación de datos de entrada

### 3. Carrito de Compras

El módulo `comprasMan.py` implementa:

- Agregar productos al carrito
- Visualización del carrito actual
- Cálculo automático del total a pagar
- Eliminación de productos del carrito
- Persistencia del estado del carrito

### 4. Gestión de Pedidos

Funcionalidades del módulo `pedidos.py`:

- **Guardar pedidos**: Persistencia del pedido actual asociado al usuario
- **Cargar pedidos**: Recuperación de pedidos previamente guardados
- **Historial**: Almacenamiento de pedidos por usuario
- **Formato de pedido**: Estructura que incluye productos, cantidades y total

## Tecnologías Utilizadas

### Lenguaje de Programación
- **Python 3.x**: Lenguaje principal del proyecto

### Bibliotecas Estándar
- `json`: Manejo de archivos JSON para persistencia de datos
- `os`: Operaciones del sistema operativo (limpieza de pantalla)
- `sys`: Gestión de rutas y configuración del sistema

### Características de Python Utilizadas
- **Pattern Matching** (`match-case`): Manejo de opciones de menú
- **Docstrings**: Documentación exhaustiva de funciones y módulos
- **Manejo de excepciones**: Control de errores robusto
- **Variables globales**: Gestión del estado de la aplicación
- **Funciones de orden superior**: Modularidad y reutilización de código

## Almacenamiento de Datos

### Estructura de `cliente.json`

```json
{
  "clientes": [
    {
      "id": 1,
      "nombre": "usuario",
      "admin": false,
      "pedidos": []
    }
  ]
}
```

### Estructura de `productos.json`

```json
{
  "pizzas": [
    {
      "code": "P001",
      "nombre": "Pizza Margarita",
      "precio": 15000
    }
  ],
  "bebidas": [...],
  "adiciones": [...],
  "salsas": [...],
  "toppings": [...]
}
```

## Instalación y Configuración

### Requisitos Previos

- Python 3.10 o superior (requerido para `match-case`)
- Sistema operativo: Linux, Windows o macOS

### Pasos de Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/sephty/RestaurantProject.git
   cd RestaurantProject
   ```

2. **Verificar archivos de datos**
   
   Asegurarse de que existen los archivos:
   - `cliente.json`
   - `productos.json`

3. **Ejecutar la aplicación**
   ```bash
   python main.py
   ```

### Configuración Inicial

Al iniciar por primera vez:
1. El sistema solicitará autenticación
2. Opción de crear una cuenta nueva
3. Opción de continuar como invitado
4. Para acceso administrativo, se requiere una cuenta con `"admin": true` en `cliente.json`

## Manual de Usuario

### Navegación del Sistema

#### Menú Principal
```
1. Pizzas          - Catálogo de pizzas disponibles
2. Bebidas         - Catálogo de bebidas
3. Adiciones       - Extras para pedidos
4. Salsas          - Salsas disponibles
5. Guardar Pedido  - Persistir el pedido actual
6. Cargar Pedido   - Recuperar pedido guardado
7. Eliminar Compra - Remover productos del carrito
8. Gestionar Productos (Admin) - Solo para administradores
0. Salir          - Finalizar la aplicación
```

#### Flujo de Trabajo Típico

1. **Inicio de sesión**: Autenticarse o continuar como invitado
2. **Selección de productos**: Navegar por los diferentes menús de productos
3. **Agregar al carrito**: Seleccionar productos deseados
4. **Revisión del pedido**: Verificar el total y los productos en el carrito
5. **Guardar pedido**: Persistir el pedido para futuras referencias
6. **Finalización**: Salir del sistema

### Funcionalidades Administrativas

Los usuarios con permisos de administrador pueden:

1. **Agregar productos**:
   - Seleccionar tipo de producto
   - Ingresar nombre y precio
   - El sistema genera automáticamente el código único

2. **Modificar productos**:
   - Listar productos de una categoría
   - Seleccionar por código
   - Actualizar nombre y/o precio

3. **Eliminar productos**:
   - Seleccionar categoría
   - Confirmar eliminación
   - Persistencia automática de cambios

## Aspectos Técnicos

### Generación de Códigos Únicos

El sistema implementa un algoritmo para generar códigos únicos:

```python
def get_next_code(tipo):
    # Prefijo según tipo: P=Pizza, B=Bebida, A=Adición, T=Topping, S=Salsa
    # Formato: [PREFIJO][NNN] (ej: P001, B023)
    # Genera el siguiente número disponible
```

### Persistencia de Datos

Implementación del módulo `fileHandler.py`:

- **Lectura de JSON**: `load_json(filepath)`
- **Escritura de JSON**: `save_json(filepath, data)`
- **Manejo de errores**: Gestión de archivos inexistentes o corruptos
- **Codificación**: UTF-8 para soporte de caracteres especiales

### Seguridad y Validación

1. **Validación de entrada**: Verificación de tipos de datos
2. **Prevención de valores negativos**: En precios y cantidades
3. **Confirmación de operaciones críticas**: Antes de eliminar datos
4. **Manejo de excepciones**: Try-except en operaciones críticas

## Limitaciones y Trabajo Futuro

### Limitaciones Actuales

1. **Base de datos**: Uso de archivos JSON en lugar de base de datos relacional
2. **Seguridad**: Sin encriptación de contraseñas
3. **Concurrencia**: No soporta múltiples usuarios simultáneos
4. **Interfaz**: Limitada a línea de comandos
5. **Validación**: Controles básicos de integridad de datos

### Mejoras Propuestas

1. **Migración a base de datos**: Implementar SQLite o PostgreSQL
2. **Sistema de autenticación robusto**: Hash de contraseñas con bcrypt
3. **Interfaz gráfica**: Desarrollo de GUI con Tkinter o PyQt
4. **API REST**: Exposición de funcionalidades mediante endpoints HTTP
5. **Reportes**: Generación de informes de ventas y estadísticas
6. **Pagos**: Integración con pasarelas de pago
7. **Notificaciones**: Sistema de alertas para administradores
8. **Testing**: Implementación de pruebas unitarias y de integración

## Casos de Uso

### Caso de Uso 1: Cliente Realiza un Pedido

**Actor**: Cliente  
**Precondición**: El sistema está en ejecución  
**Flujo Principal**:
1. Cliente inicia sesión o continúa como invitado
2. Cliente navega al menú de pizzas
3. Cliente selecciona una pizza
4. El producto se agrega al carrito
5. Cliente navega al menú de bebidas
6. Cliente selecciona una bebida
7. Cliente revisa el total del pedido
8. Cliente guarda el pedido
9. Cliente finaliza la sesión

### Caso de Uso 2: Administrador Gestiona Productos

**Actor**: Administrador  
**Precondición**: Usuario con permisos de admin autenticado  
**Flujo Principal**:
1. Administrador accede al menú de gestión
2. Selecciona "Agregar Producto"
3. Especifica tipo: pizza
4. Ingresa nombre: "Pizza Vegetariana"
5. Ingresa precio: 18000
6. Sistema genera código P004
7. Producto agregado exitosamente
8. Administrador regresa al menú principal



- **Repositorio**: https://github.com/sephty/RestaurantProject.git
- **Autor**: Joseph Garcia Jimenez


