# Módulo de Gestión de Biblioteca para Odoo 18

Sistema completo de gestión de biblioteca que permite administrar libros, préstamos y miembros.

## Características

- ✅ Gestión de catálogo de libros
- ✅ Control de copias físicas de libros
- ✅ Sistema de préstamos con fechas de vencimiento
- ✅ Gestión de miembros de la biblioteca
- ✅ Historial de préstamos
- ✅ Notificaciones y seguimiento (integración con mail)
- ✅ API Key para autenticación de usuarios
- ✅ API REST (JSON-RPC nativa de Odoo)

## Instalación

1. Copiar el módulo a la carpeta `addons` de Odoo
2. Actualizar la lista de módulos desde la interfaz de Odoo
3. Instalar el módulo "Gestión de Biblioteca"

## Uso de la Interfaz Web

Una vez instalado, encontrarás un nuevo menú "Biblioteca" con las siguientes opciones:

### Catálogo

- **Libros**: Gestiona el catálogo maestro de libros

### Operaciones

- **Préstamos**: Registra y gestiona préstamos de libros

### Configuración

- **Miembros**: Administra los miembros de la biblioteca

## API REST - JSON-RPC (Nativa de Odoo)

Odoo proporciona una API JSON-RPC nativa que funciona de forma estándar y es la recomendada para integraciones externas.

### Autenticación

```python
import xmlrpc.client

url = 'http://localhost:8069'
db = 'odoo'
username = 'admin'
password = 'admin'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
```

### Ejemplos de Uso con Python

#### 1. Buscar Libros

```python
import xmlrpc.client

url = 'http://localhost:8069'
db = 'odoo'
username = 'admin'
password = 'admin'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

books = models.execute_kw(db, uid, password,
    'library.book', 'search_read',
    [[['name', 'ilike', 'Python']]],
    {'fields': ['id', 'name', 'isbn', 'availability']}
)

print(books)
```

#### 2. Crear un Nuevo Libro

```python
book_id = models.execute_kw(db, uid, password,
    'library.book', 'create',
    [{
        'name': 'El Principito',
        'isbn': '9788498382679',
    }]
)

print(f"Libro creado con ID: {book_id}")
```

#### 3. Crear un Préstamo

```python
loan_id = models.execute_kw(db, uid, password,
    'library.loan', 'create',
    [{
        'member_id': 7,  # ID del miembro
        'copy_id': 3,    # ID de la copia del libro
        'loan_date': '2025-01-20',
        'due_date': '2025-02-03',
    }]
)

print(f"Préstamo creado con ID: {loan_id}")
```

#### 4. Confirmar un Préstamo

```python
models.execute_kw(db, uid, password,
    'library.loan', 'action_loan',
    [[loan_id]]
)
```

#### 5. Registrar Devolución

```python
models.execute_kw(db, uid, password,
    'library.loan', 'action_return',
    [[loan_id]]
)
```

### Uso con cURL (JSON-RPC)

#### Autenticación

```bash
curl -X POST \
    -H "Content-Type: application/json" \
    -d '{
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "service": "common",
            "method": "authenticate",
            "args": ["odoo", "admin", "admin", {}]
        },
        "id": 1
    }' \
    http://localhost:8069/jsonrpc
```

#### Buscar Libros

```bash
curl -X POST \
    -H "Content-Type: application/json" \
    -d '{
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "service": "object",
            "method": "execute_kw",
            "args": [
                "odoo",
                2,
                "admin",
                "library.book",
                "search_read",
                [[]],
                {"fields": ["id", "name", "isbn", "availability"], "limit": 10}
            ]
        },
        "id": 2
    }' \
    http://localhost:8069/jsonrpc
```

### Uso con JavaScript/Node.js

```javascript
const axios = require('axios');

const odooUrl = 'http://localhost:8069';
const db = 'odoo';
const username = 'admin';
const password = 'admin';

async function authenticate() {
    const response = await axios.post(`${odooUrl}/jsonrpc`, {
        jsonrpc: '2.0',
        method: 'call',
        params: {
            service: 'common',
            method: 'authenticate',
            args: [db, username, password, {}]
        },
        id: 1
    });
    return response.data.result;
}

async function searchBooks(uid) {
    const response = await axios.post(`${odooUrl}/jsonrpc`, {
        jsonrpc: '2.0',
        method: 'call',
        params: {
            service: 'object',
            method: 'execute_kw',
            args: [
                db,
                uid,
                password,
                'library.book',
                'search_read',
                [[]],
                {fields: ['id', 'name', 'isbn', 'availability'], limit: 10}
            ]
        },
        id: 2
    });
    return response.data.result;
}

(async () => {
    const uid = await authenticate();
    console.log('Authenticated with UID:', uid);
    
    const books = await searchBooks(uid);
    console.log('Books:', books);
})();
```

## Modelos Disponibles

### library.book

- `name`: Título del libro (requerido)
- `author_ids`: Autores (Many2many con res.partner)
- `isbn`: ISBN del libro
- `sinopsis`: Descripción del libro
- `copy_ids`: Copias físicas del libro
- `availability`: Estado de disponibilidad (calculado)

### library.book.copy

- `book_id`: Libro al que pertenece (requerido)
- `reference_code`: Código único de la copia (requerido)
- `state`: Estado (available, on_loan, reserved, lost)

### library.loan

- `member_id`: Miembro que realiza el préstamo (requerido)
- `copy_id`: Copia del libro prestada (requerido)
- `book_id`: Libro (calculado automáticamente)
- `loan_date`: Fecha de préstamo
- `due_date`: Fecha de vencimiento
- `return_date`: Fecha de devolución
- `state`: Estado (draft, active, overdue, returned)

### res.partner (extensión)

- `is_library_member`: Indica si es miembro de la biblioteca
- `member_id_code`: Código de miembro
- `loan_ids`: Histórico de préstamos

### res.users (extensión)

- `api_key`: Clave API para autenticación externa

## Seguridad

El módulo incluye reglas de acceso configuradas:

- Usuarios regulares: Lectura en todos los modelos
- Administradores (Settings): Acceso completo

## Notas Técnicas

### Controladores HTTP Personalizados

El módulo incluye controladores HTTP personalizados en `controllers/book_api.py`, sin embargo, debido a limitaciones
conocidas en Odoo 18, estos controladores pueden no registrarse automáticamente. Se recomienda usar la API JSON-RPC
nativa de Odoo para integraciones externas, que es más robusta y está mejor soportada.

### Dependencias

- `base`: Módulo base de Odoo
- `mail`: Sistema de mensajería y notificaciones
- `web`: Módulo web de Odoo

## Soporte

Para problemas o preguntas, consulta la documentación oficial de Odoo:

- [Odoo External API](https://www.odoo.com/documentation/18.0/developer/reference/external_api.html)
- [Odoo Web Controllers](https://www.odoo.com/documentation/18.0/developer/reference/backend/http.html)

## Licencia

LGPL-3
