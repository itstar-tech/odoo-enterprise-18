# 📚 Documentación de API - Sistema de Gestión de Biblioteca

## 🚀 Estado del Servicio

**URL Base**: `http://localhost:8069`  
**Base de Datos**: `library_management`  
**Puerto**: `8069`

## 🎯 Pruebas con Postman

**¿Prefieres probar la API con Postman?** Tenemos una guía completa para ti:

- 📖 **[Guía de Postman](POSTMAN_GUIDE.md)** - Documentación paso a paso
- 📦 **[Colección de Postman](postman_collection.json)** - Archivo listo para importar

### Importar Colección de Postman

1. Abre Postman
2. Click en **"Import"**
3. Selecciona el archivo `postman_collection.json`
4. ¡Listo! Todas las peticiones están configuradas

La colección incluye:

- ✅ 14+ peticiones pre-configuradas
- ✅ Tests automáticos
- ✅ Variables de entorno
- ✅ Ejemplos de todas las operaciones CRUD

## 🔑 Autenticación

La API de Odoo utiliza autenticación mediante usuario y contraseña para obtener un UID (User ID) que se usa en todas las
operaciones subsecuentes.

### Credenciales por Defecto

```
Usuario: admin
Contraseña: admin
Base de Datos: library_management
```

## 📡 Endpoints Disponibles

### 1. Autenticación

- **URL**: `http://localhost:8069/xmlrpc/2/common`
- **Método**: `authenticate`
- **Propósito**: Obtener el UID del usuario

### 2. Operaciones de Modelos

- **URL**: `http://localhost:8069/xmlrpc/2/object`
- **Método**: `execute_kw`
- **Propósito**: Realizar operaciones CRUD en cualquier modelo

### 3. JSON-RPC (Alternativa)

- **URL**: `http://localhost:8069/jsonrpc`
- **Método**: POST con JSON
- **Propósito**: API JSON-RPC estándar

## 🐍 Ejemplos con Python

### Instalación de Dependencias

```bash
# No requiere dependencias adicionales, usa la biblioteca estándar
python3 --version  # Debe ser Python 3.6+
```

### Ejemplo Completo - Gestión de Libros

```python
#!/usr/bin/env python3
"""
Ejemplo completo de uso de la API de Gestión de Biblioteca
"""
import xmlrpc.client

# Configuración
URL = 'http://localhost:8069'
DB = 'library_management'
USERNAME = 'admin'
PASSWORD = 'admin'

# 1. AUTENTICACIÓN
print("=" * 60)
print("1. AUTENTICANDO EN ODOO")
print("=" * 60)

common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
uid = common.authenticate(DB, USERNAME, PASSWORD, {})

if not uid:
    print("❌ Error de autenticación")
    exit(1)

print(f"✅ Autenticado exitosamente. UID: {uid}")
print()

# Cliente de modelos
models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')

# 2. LISTAR TODOS LOS LIBROS
print("=" * 60)
print("2. LISTANDO LIBROS")
print("=" * 60)

books = models.execute_kw(DB, uid, PASSWORD,
    'library.book', 'search_read',
    [[]],
    {'fields': ['id', 'name', 'isbn', 'availability'], 'limit': 10}
)

print(f"📚 Se encontraron {len(books)} libro(s):")
for book in books:
    print(f"  ID: {book['id']}")
    print(f"  Título: {book['name']}")
    print(f"  ISBN: {book.get('isbn', 'N/A')}")
    print(f"  Disponibilidad: {book['availability']}")
    print("-" * 40)
print()

# 3. CREAR UN NUEVO LIBRO
print("=" * 60)
print("3. CREANDO UN NUEVO LIBRO")
print("=" * 60)

new_book_data = {
    'name': 'Cien Años de Soledad',
    'isbn': '9780307474728',
}

try:
    new_book_id = models.execute_kw(DB, uid, PASSWORD,
        'library.book', 'create',
        [new_book_data]
    )
    print(f"✅ Libro creado exitosamente con ID: {new_book_id}")
except Exception as e:
    print(f"⚠️  Error al crear libro: {e}")
print()

# 4. BUSCAR LIBRO ESPECÍFICO
print("=" * 60)
print("4. BUSCANDO LIBRO POR NOMBRE")
print("=" * 60)

search_term = 'Soledad'
found_books = models.execute_kw(DB, uid, PASSWORD,
    'library.book', 'search_read',
    [[['name', 'ilike', search_term]]],
    {'fields': ['id', 'name', 'isbn']}
)

print(f"🔍 Búsqueda de '{search_term}':")
for book in found_books:
    print(f"  - {book['name']} (ID: {book['id']})")
print()

# 5. ACTUALIZAR UN LIBRO
print("=" * 60)
print("5. ACTUALIZANDO UN LIBRO")
print("=" * 60)

if books:
    book_to_update = books[0]['id']
    update_data = {
        'isbn': '9999999999999'
    }
    
    try:
        models.execute_kw(DB, uid, PASSWORD,
            'library.book', 'write',
            [[book_to_update], update_data]
        )
        print(f"✅ Libro ID {book_to_update} actualizado")
    except Exception as e:
        print(f"⚠️  Error al actualizar: {e}")
print()

# 6. LISTAR COPIAS DE LIBROS
print("=" * 60)
print("6. LISTANDO COPIAS DE LIBROS")
print("=" * 60)

copies = models.execute_kw(DB, uid, PASSWORD,
    'library.book.copy', 'search_read',
    [[]],
    {'fields': ['id', 'reference_code', 'state', 'book_id'], 'limit': 5}
)

print(f"📦 Se encontraron {len(copies)} copia(s):")
for copy in copies:
    book_name = copy['book_id'][1] if copy.get('book_id') else 'N/A'
    print(f"  Código: {copy['reference_code']}")
    print(f"  Estado: {copy['state']}")
    print(f"  Libro: {book_name}")
    print("-" * 40)
print()

# 7. LISTAR PRÉSTAMOS
print("=" * 60)
print("7. LISTANDO PRÉSTAMOS")
print("=" * 60)

loans = models.execute_kw(DB, uid, PASSWORD,
    'library.loan', 'search_read',
    [[]],
    {'fields': ['id', 'member_id', 'book_id', 'state', 'loan_date', 'due_date'], 'limit': 5}
)

print(f"📋 Se encontraron {len(loans)} préstamo(s):")
for loan in loans:
    member_name = loan['member_id'][1] if loan.get('member_id') else 'N/A'
    book_name = loan['book_id'][1] if loan.get('book_id') else 'N/A'
    print(f"  Préstamo ID: {loan['id']}")
    print(f"  Miembro: {member_name}")
    print(f"  Libro: {book_name}")
    print(f"  Estado: {loan['state']}")
    print(f"  Fecha préstamo: {loan.get('loan_date', 'N/A')}")
    print(f"  Fecha vencimiento: {loan.get('due_date', 'N/A')}")
    print("-" * 40)
print()

# 8. CONTAR REGISTROS
print("=" * 60)
print("8. ESTADÍSTICAS")
print("=" * 60)

total_books = models.execute_kw(DB, uid, PASSWORD,
    'library.book', 'search_count', [[]]
)

total_copies = models.execute_kw(DB, uid, PASSWORD,
    'library.book.copy', 'search_count', [[]]
)

total_loans = models.execute_kw(DB, uid, PASSWORD,
    'library.loan', 'search_count', [[]]
)

active_loans = models.execute_kw(DB, uid, PASSWORD,
    'library.loan', 'search_count',
    [[['state', '=', 'active']]]
)

print(f"📊 Estadísticas del Sistema:")
print(f"  Total de libros: {total_books}")
print(f"  Total de copias: {total_copies}")
print(f"  Total de préstamos: {total_loans}")
print(f"  Préstamos activos: {active_loans}")
print()

print("=" * 60)
print("✅ PRUEBA COMPLETADA EXITOSAMENTE")
print("=" * 60)
```

## 🌐 Ejemplos con cURL

### 1. Autenticación

```bash
curl -X POST http://localhost:8069/jsonrpc \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
      "service": "common",
      "method": "authenticate",
      "args": ["library_management", "admin", "admin", {}]
    },
    "id": 1
  }' | jq
```

### 2. Listar Libros

```bash
# Primero obtén el UID de la autenticación (ej: 2)
curl -X POST http://localhost:8069/jsonrpc \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
      "service": "object",
      "method": "execute_kw",
      "args": [
        "library_management",
        2,
        "admin",
        "library.book",
        "search_read",
        [[]],
        {"fields": ["id", "name", "isbn", "availability"], "limit": 10}
      ]
    },
    "id": 2
  }' | jq
```

### 3. Crear un Libro

```bash
curl -X POST http://localhost:8069/jsonrpc \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
      "service": "object",
      "method": "execute_kw",
      "args": [
        "library_management",
        2,
        "admin",
        "library.book",
        "create",
        [{"name": "El Quijote", "isbn": "9788491050360"}]
      ]
    },
    "id": 3
  }' | jq
```

### 4. Buscar Libros por Nombre

```bash
curl -X POST http://localhost:8069/jsonrpc \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
      "service": "object",
      "method": "execute_kw",
      "args": [
        "library_management",
        2,
        "admin",
        "library.book",
        "search_read",
        [[["name", "ilike", "Quijote"]]],
        {"fields": ["id", "name", "isbn"]}
      ]
    },
    "id": 4
  }' | jq
```

## 💻 Ejemplos con JavaScript/Node.js

### Instalación

```bash
npm install axios
```

### Código Completo

```javascript
const axios = require('axios');

const ODOO_URL = 'http://localhost:8069';
const DB = 'library_management';
const USERNAME = 'admin';
const PASSWORD = 'admin';

class OdooAPI {
    constructor(url, db, username, password) {
        this.url = url;
        this.db = db;
        this.username = username;
        this.password = password;
        this.uid = null;
    }

    async authenticate() {
        const response = await axios.post(`${this.url}/jsonrpc`, {
            jsonrpc: '2.0',
            method: 'call',
            params: {
                service: 'common',
                method: 'authenticate',
                args: [this.db, this.username, this.password, {}]
            },
            id: 1
        });
        this.uid = response.data.result;
        return this.uid;
    }

    async execute(model, method, args, kwargs = {}) {
        const response = await axios.post(`${this.url}/jsonrpc`, {
            jsonrpc: '2.0',
            method: 'call',
            params: {
                service: 'object',
                method: 'execute_kw',
                args: [
                    this.db,
                    this.uid,
                    this.password,
                    model,
                    method,
                    args,
                    kwargs
                ]
            },
            id: Math.floor(Math.random() * 1000)
        });
        return response.data.result;
    }

    // Métodos específicos para la biblioteca
    async searchBooks(searchTerm = null) {
        const domain = searchTerm ? [['name', 'ilike', searchTerm]] : [];
        return await this.execute(
            'library.book',
            'search_read',
            [domain],
            { fields: ['id', 'name', 'isbn', 'availability'], limit: 10 }
        );
    }

    async createBook(name, isbn = null) {
        return await this.execute(
            'library.book',
            'create',
            [{ name, isbn }]
        );
    }

    async getLoans() {
        return await this.execute(
            'library.loan',
            'search_read',
            [[]],
            { fields: ['id', 'member_id', 'book_id', 'state', 'loan_date', 'due_date'], limit: 10 }
        );
    }

    async getStatistics() {
        const totalBooks = await this.execute('library.book', 'search_count', [[]]);
        const totalCopies = await this.execute('library.book.copy', 'search_count', [[]]);
        const totalLoans = await this.execute('library.loan', 'search_count', [[]]);
        const activeLoans = await this.execute('library.loan', 'search_count', [[['state', '=', 'active']]]);
        
        return { totalBooks, totalCopies, totalLoans, activeLoans };
    }
}

// Uso
(async () => {
    try {
        const api = new OdooAPI(ODOO_URL, DB, USERNAME, PASSWORD);
        
        console.log('🔑 Autenticando...');
        await api.authenticate();
        console.log(`✅ Autenticado con UID: ${api.uid}\n`);
        
        console.log('📚 Listando libros...');
        const books = await api.searchBooks();
        console.log(`Encontrados ${books.length} libro(s):`);
        books.forEach(book => {
            console.log(`  - ${book.name} (ID: ${book.id})`);
        });
        console.log();
        
        console.log('📊 Obteniendo estadísticas...');
        const stats = await api.getStatistics();
        console.log('Estadísticas:');
        console.log(`  Total libros: ${stats.totalBooks}`);
        console.log(`  Total copias: ${stats.totalCopies}`);
        console.log(`  Préstamos activos: ${stats.activeLoans}`);
        console.log();
        
        console.log('✅ Prueba completada exitosamente');
    } catch (error) {
        console.error('❌ Error:', error.message);
        if (error.response) {
            console.error('Detalles:', error.response.data);
        }
    }
})();
```

## 📋 Modelos y Campos Disponibles

### library.book (Libros)

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | Integer | ID único |
| `name` | String | Título del libro (requerido) |
| `author_ids` | Many2many | Autores del libro |
| `isbn` | String | Código ISBN |
| `sinopsis` | Text | Descripción del libro |
| `copy_ids` | One2many | Copias físicas |
| `availability` | Selection | Estado: available, on_loan, not_available |

### library.book.copy (Copias Físicas)

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | Integer | ID único |
| `book_id` | Many2one | Libro al que pertenece (requerido) |
| `reference_code` | String | Código de referencia único (requerido) |
| `state` | Selection | Estado: available, on_loan, reserved, lost |

### library.loan (Préstamos)

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | Integer | ID único |
| `member_id` | Many2one | Miembro (requerido) |
| `copy_id` | Many2one | Copia del libro (requerido) |
| `book_id` | Many2one | Libro (calculado automáticamente) |
| `loan_date` | Date | Fecha de préstamo |
| `due_date` | Date | Fecha de vencimiento (requerido) |
| `return_date` | Date | Fecha de devolución |
| `state` | Selection | Estado: draft, active, returned, overdue |

### Métodos de Acción Disponibles

- `library.loan.action_loan()` - Confirmar préstamo
- `library.loan.action_return()` - Registrar devolución

## 🧪 Pruebas Rápidas

### Test 1: Verificar Conectividad

```bash
curl -s http://localhost:8069/web/database/selector | head -5
```

Debe retornar HTML de la página de selección de base de datos.

### Test 2: Autenticación XML-RPC

```python
python3 -c "
import xmlrpc.client
common = xmlrpc.client.ServerProxy('http://localhost:8069/xmlrpc/2/common')
uid = common.authenticate('library_management', 'admin', 'admin', {})
print(f'UID: {uid}')
"
```

### Test 3: Contar Libros

```python
python3 -c "
import xmlrpc.client
common = xmlrpc.client.ServerProxy('http://localhost:8069/xmlrpc/2/common')
uid = common.authenticate('library_management', 'admin', 'admin', {})
models = xmlrpc.client.ServerProxy('http://localhost:8069/xmlrpc/2/object')
count = models.execute_kw('library_management', uid, 'admin', 'library.book', 'search_count', [[]])
print(f'Total de libros: {count}')
"
```

## 🔧 Troubleshooting

### Error: Connection Refused

```bash
# Verificar que Odoo esté corriendo
docker compose ps

# Reiniciar si es necesario
docker compose restart odoo
```

### Error: Authentication Failed

- Verificar credenciales (usuario/contraseña)
- Verificar nombre de la base de datos
- Asegurarse de que el usuario existe y está activo

### Error: Model Not Found

- Verificar que el módulo `library_management` esté instalado
- Actualizar el módulo si es necesario:

```bash
docker compose exec -T odoo odoo -d library_management -u library_management --stop-after-init
docker compose restart odoo
```

## 📞 Información de Contacto

- **URL del Servicio**: http://localhost:8069
- **Puerto Base de Datos**: 5433 (PostgreSQL)
- **Documentación Oficial**: https://www.odoo.com/documentation/18.0/

## ✅ Checklist de Implementación

- [x] API REST configurada y funcionando
- [x] Autenticación implementada
- [x] CRUD completo de libros
- [x] Sistema de préstamos operativo
- [x] Gestión de copias físicas
- [x] Documentación completa
- [x] Ejemplos en múltiples lenguajes
- [x] Tests de conectividad

---

**Última actualización**: 2025-01-24  
**Versión de Odoo**: 18.0  
**Módulo**: library_management v1.0
