# Guía de API JSON-RPC - Library Management

## Descripción

Esta API usa el protocolo JSON-RPC estándar de Odoo. En lugar de crear endpoints personalizados, usa el endpoint
estándar `/jsonrpc` de Odoo con métodos de nuestro controlador.

**IMPORTANTE**: Debido a las limitaciones de Odoo, las rutas JSON-RPC personalizadas (como `/api/library/ping`) no
funcionan correctamente. La API usa métodos del controlador que se acceden a través del ORM de Odoo.

## Uso Recomendado

Para usar esta API, tienes dos opciones:

### Opción 1: Usar bibliotecas de Python como OdooRPC (RECOMENDADO)

```bash
pip install odoorpc
```

```python
import odoorpc

odoo = odoorpc.ODOO('localhost', port=8069)

odoo.login('library_management', 'admin', 'admin')

Book = odoo.env['library.book']

books = Book.search([])
print(f"Libros encontrados: {len(books)}")

for book_id in books[:5]:
    book_data = Book.read(book_id, ['name', 'isbn', 'availability'])
    print(f"  - {book_data['name']}")

new_book_id = Book.create({
    'name': 'El Principito',
    'isbn': '978-0156012195'
})
print(f"Libro creado con ID: {new_book_id}")

Book.write([new_book_id], {
    'name': 'El Principito (Edición Actualizada)'
})

Book.unlink([new_book_id])
print("Libro eliminado")
```

### Opción 2: Usar el endpoint /jsonrpc estándar de Odoo

```python
import json
import random
import urllib.request

HOST = 'localhost'
PORT = 8069
DB = 'library_management'
USER = 'admin'
PASSWORD = 'admin'

def json_rpc(url, service, method, *args):
    data = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "service": service,
            "method": method,
            "args": args
        },
        "id": random.randint(0, 1000000000),
    }
    req = urllib.request.Request(
        url=url,
        data=json.dumps(data).encode(),
        headers={"Content-Type": "application/json"}
    )
    reply = json.loads(urllib.request.urlopen(req).read().decode('UTF-8'))
    if reply.get("error"):
        raise Exception(reply["error"])
    return reply.get("result")

url = f"http://{HOST}:{PORT}/jsonrpc"

uid = json_rpc(url, "common", "login", DB, USER, PASSWORD)
print(f"UID: {uid}")

books = json_rpc(url, "object", "execute", DB, uid, PASSWORD, 
                 'library.book', 'search_read', [], ['name', 'isbn'])
print(f"Libros: {books}")

new_id = json_rpc(url, "object", "execute", DB, uid, PASSWORD,
                  'library.book', 'create', {
                      'name': 'El Principito',
                      'isbn': '978-0156012195'
                  })
print(f"Nuevo libro ID: {new_id}")

json_rpc(url, "object", "execute", DB, uid, PASSWORD,
         'library.book', 'write', [new_id], {
             'name': 'El Principito (Actualizado)'
         })

json_rpc(url, "object", "execute", DB, uid, PASSWORD,
         'library.book', 'unlink', [new_id])
```

## Configuración

### Credenciales predeterminadas

```python
HOST = 'localhost'
PORT = 8069
DB = 'library_management'
USER = 'admin'
PASSWORD = 'admin'
```

## Operaciones CRUD

### 1. Autenticación

```python
uid = json_rpc(url, "common", "login", DB, USER, PASSWORD)
```

### 2. Buscar libros (search_read)

```python
books = json_rpc(url, "object", "execute", DB, uid, PASSWORD,
                 'library.book', 'search_read', 
                 [('name', 'ilike', 'Quijote')],
                 ['id', 'name', 'isbn', 'availability'])
```

### 3. Crear libro

```python
new_id = json_rpc(url, "object", "execute", DB, uid, PASSWORD,
                  'library.book', 'create', {
                      'name': 'El Principito',
                      'isbn': '978-0156012195'
                  })
```

### 4. Leer libro

```python
book_data = json_rpc(url, "object", "execute", DB, uid, PASSWORD,
                     'library.book', 'read', [book_id],
                     ['id', 'name', 'isbn', 'availability'])
```

### 5. Actualizar libro

```python
json_rpc(url, "object", "execute", DB, uid, PASSWORD,
         'library.book', 'write', [book_id], {
             'name': 'Nuevo nombre',
             'isbn': '9876543210'
         })
```

### 6. Eliminar libro

```python
json_rpc(url, "object", "execute", DB, uid, PASSWORD,
         'library.book', 'unlink', [book_id])
```

## Script de Ejemplo Completo

Archivo: `addons/library_management/examples/test_jsonrpc_standard.py`

```python
#!/usr/bin/env python3
import json
import random
import urllib.request

HOST = 'localhost'
PORT = 8069
DB = 'library_management'
USER = 'admin'
PASSWORD = 'admin'

def json_rpc(url, service, method, *args):
    data = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "service": service,
            "method": method,
            "args": args
        },
        "id": random.randint(0, 1000000000),
    }
    req = urllib.request.Request(
        url=url,
        data=json.dumps(data).encode(),
        headers={"Content-Type": "application/json"}
    )
    reply = json.loads(urllib.request.urlopen(req).read().decode('UTF-8'))
    if reply.get("error"):
        raise Exception(reply["error"])
    return reply.get("result")

def main():
    url = f"http://{HOST}:{PORT}/jsonrpc"
    
    print("1. Autenticación...")
    uid = json_rpc(url, "common", "login", DB, USER, PASSWORD)
    print(f"   UID: {uid}")
    
    print("\n2. Buscar libros...")
    books = json_rpc(url, "object", "execute", DB, uid, PASSWORD,
                     'library.book', 'search_read', [],
                     ['id', 'name', 'isbn', 'availability'],
                     {'limit': 5})
    print(f"   Encontrados: {len(books)} libros")
    for book in books[:3]:
        print(f"      - {book['name']}")
    
    print("\n3. Crear libro...")
    new_id = json_rpc(url, "object", "execute", DB, uid, PASSWORD,
                      'library.book', 'create', {
                          'name': 'El Principito',
                          'isbn': '978-0156012195'
                      })
    print(f"   Libro creado con ID: {new_id}")
    
    print("\n4. Leer libro...")
    book_data = json_rpc(url, "object", "execute", DB, uid, PASSWORD,
                         'library.book', 'read', [new_id],
                         ['id', 'name', 'isbn', 'availability'])
    print(f"   Datos: {book_data[0]}")
    
    print("\n5. Actualizar libro...")
    json_rpc(url, "object", "execute", DB, uid, PASSWORD,
             'library.book', 'write', [new_id], {
                 'name': 'El Principito (Edición Actualizada)'
             })
    print(f"   Libro actualizado")
    
    print("\n6. Eliminar libro...")
    json_rpc(url, "object", "execute", DB, uid, PASSWORD,
             'library.book', 'unlink', [new_id])
    print(f"   Libro eliminado")
    
    print("\n Todos los tests completados exitosamente!")

if __name__ == '__main__':
    main()
```

## Usando con curl

### Autenticación

```bash
curl -X POST http://localhost:8069/jsonrpc \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
      "service": "common",
      "method": "login",
      "args": ["library_management", "admin", "admin"]
    },
    "id": 1
  }'
```

### Buscar libros

```bash
curl -X POST http://localhost:8069/jsonrpc \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
      "service": "object",
      "method": "execute",
      "args": ["library_management", 2, "admin", "library.book", "search_read", [], ["name", "isbn"]]
    },
    "id": 1
  }'
```

## Usando con bibliotecas de Python

### OdooRPC (RECOMENDADO)

```bash
pip install odoorpc
```

```python
import odoorpc

odoo = odoorpc.ODOO('localhost', port=8069)
odoo.login('library_management', 'admin', 'admin')

Book = odoo.env['library.book']
books = Book.search([])
for book_id in books:
    book = Book.browse(book_id)
    print(f"- {book.name}")
```

## Solución de Problemas

### Error: "Credenciales inválidas"

- Verifica que el usuario y contraseña sean correctos
- Verifica que el nombre de la base de datos sea correcto
- Verifica que el usuario esté activo en Odoo

### Error: "404 Not Found"

- Si intentas usar rutas personalizadas como `/api/library/ping`, no funcionarán
- Usa el endpoint estándar `/jsonrpc` de Odoo

### Error: "Session expired"

- Vuelve a autenticarte usando el método `login`
- Asegúrate de pasar el UID correcto en cada llamada

## Seguridad

- **Nunca expongas credenciales en el código público**
- **Usa HTTPS en producción**
- **Configura permisos de usuario apropiados**
- **Considera usar tokens JWT para APIs públicas**

## Referencias

- [Documentación oficial Odoo JSON-RPC](https://www.odoo.com/documentation/16.0/developer/reference/external_api.html#json-rpc-library)
- [OdooRPC Library](https://pythonhosted.org/OdooRPC/)
- [API Externa Odoo](https://www.odoo.com/documentation/16.0/developer/reference/external_api.html)
