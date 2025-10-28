# Ejemplos de Uso de la API

Esta carpeta contiene scripts de ejemplo para interactuar con la API REST de Gestión de Biblioteca.

## Scripts Disponibles

### `test_api.py`

Script interactivo para probar todos los endpoints de la API.

#### Requisitos

```bash
pip install requests
```

#### Uso

```bash
cd addons/library_management/examples
python3 test_api.py
```

El script te pedirá:

1. Tu API Key
2. La URL de tu servidor Odoo (default: http://localhost:8069)

#### Pruebas que ejecuta

1. **Health Check**: Verifica la conectividad con el servidor
2. **Crear Libro**: Crea un libro de prueba con 3 copias
3. **Obtener Detalles**: Obtiene los detalles del libro creado
4. **Buscar Libros**: Busca libros por nombre

## Obtener una API Key

Antes de ejecutar los scripts, necesitas generar una API Key:

1. Inicia sesión en Odoo
2. Ve a tu perfil de usuario (esquina superior derecha)
3. Selecciona **Preferencias**
4. En la pestaña **Cuenta**, busca **API Keys**
5. Haz clic en **Nueva API Key**
6. Ingresa una descripción (ej: "Pruebas API")
7. Copia la clave generada

## Crear tu Propio Cliente

Puedes usar la clase `OdooLibraryClient` del script `test_api.py` como base para crear tu propia integración:

```python
from test_api import OdooLibraryClient

client = OdooLibraryClient(
    base_url="http://localhost:8069",
    api_key="tu_api_key_aqui"
)

result = client.create_book(
    name="Mi Libro",
    isbn="1234567890",
    copies=[
        {"reference_code": "COPY-001"}
    ]
)

print(result)
```

## Documentación Completa

Para más información sobre la API, consulta:

- **[../API_USAGE.md](../API_USAGE.md)** - Guía completa de uso de la API
- **[../README.md](../README.md)** - Documentación general del módulo
