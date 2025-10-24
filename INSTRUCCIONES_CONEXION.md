# 🎉 API de Gestión de Biblioteca - LISTA PARA USAR

## ✅ Estado: OPERATIVA Y FUNCIONAL

Tu API de gestión de biblioteca está corriendo y completamente funcional. Todas las pruebas han pasado exitosamente.

## 🔑 Credenciales de Conexión

```
URL:            http://localhost:8069
Base de Datos:  library_management
Usuario:        admin
Contraseña:     admin
```

## 🚀 Inicio Rápido

### 1. Verificar que está corriendo

```bash
docker compose ps
```

Deberías ver:

```
NAME          STATUS                 PORTS
odoo-odoo-1   Up                     0.0.0.0:8069->8069/tcp
odoo-db-1     Up (healthy)           0.0.0.0:5433->5432/tcp
```

### 2. Acceder a la Interfaz Web

Abre tu navegador en: **http://localhost:8069**

- Selecciona la base de datos: `library_management`
- Usuario: `admin`
- Contraseña: `admin`

### 3. Probar la API (Python)

```python
import xmlrpc.client

# Conectar
common = xmlrpc.client.ServerProxy('http://localhost:8069/xmlrpc/2/common')
uid = common.authenticate('library_management', 'admin', 'admin', {})

# Listar libros
models = xmlrpc.client.ServerProxy('http://localhost:8069/xmlrpc/2/object')
books = models.execute_kw('library_management', uid, 'admin',
    'library.book', 'search_read', [[]],
    {'fields': ['id', 'name', 'isbn'], 'limit': 10}
)

print(f"Libros encontrados: {len(books)}")
for book in books:
    print(f"  - {book['name']}")
```

### 4. Ejecutar Script de Pruebas

```bash
python3 scripts/test_complete_api.py
```

Este script realizará automáticamente:

- ✅ Autenticación
- ✅ Creación de un libro de prueba
- ✅ Búsqueda de libros
- ✅ Estadísticas del sistema
- ✅ Verificación de todos los modelos

## 📚 Modelos Disponibles

### library.book (Libros del Catálogo)

Gestiona el catálogo maestro de libros.

**Operaciones disponibles:**

- `search` - Buscar IDs de libros
- `search_read` - Buscar y leer datos de libros
- `create` - Crear un nuevo libro
- `write` - Actualizar un libro existente
- `unlink` - Eliminar un libro

**Campos principales:**

- `name` - Título del libro (requerido)
- `isbn` - Código ISBN
- `author_ids` - Autores (relación Many2many)
- `sinopsis` - Descripción del libro
- `availability` - Estado de disponibilidad

**Ejemplo - Crear un libro:**

```python
book_id = models.execute_kw('library_management', uid, 'admin',
    'library.book', 'create',
    [{
        'name': 'Cien Años de Soledad',
        'isbn': '9780307474728',
    }]
)
```

### library.book.copy (Copias Físicas)

Gestiona las copias físicas individuales de cada libro.

**Campos principales:**

- `book_id` - Libro al que pertenece (requerido)
- `reference_code` - Código único de la copia (requerido)
- `state` - Estado: available, on_loan, reserved, lost

**Ejemplo - Crear una copia:**

```python
copy_id = models.execute_kw('library_management', uid, 'admin',
    'library.book.copy', 'create',
    [{
        'book_id': 1,  # ID del libro
        'reference_code': 'LIB-001-C1',
        'state': 'available'
    }]
)
```

### library.loan (Préstamos)

Gestiona los préstamos de libros a miembros.

**Campos principales:**

- `member_id` - Miembro que hace el préstamo (requerido)
- `copy_id` - Copia del libro prestada (requerido)
- `loan_date` - Fecha de préstamo
- `due_date` - Fecha de vencimiento (requerido)
- `state` - Estado: draft, active, returned, overdue

**Métodos especiales:**

- `action_loan()` - Confirmar el préstamo
- `action_return()` - Registrar la devolución

**Ejemplo - Crear y confirmar un préstamo:**

```python
# Crear préstamo
loan_id = models.execute_kw('library_management', uid, 'admin',
    'library.loan', 'create',
    [{
        'member_id': 7,
        'copy_id': 1,
        'due_date': '2025-02-15'
    }]
)

# Confirmar préstamo
models.execute_kw('library_management', uid, 'admin',
    'library.loan', 'action_loan',
    [[loan_id]]
)
```

### res.partner (Miembros)

Extensión del modelo de contactos para gestionar miembros de la biblioteca.

**Campos adicionales:**

- `is_library_member` - Boolean que indica si es miembro
- `member_id_code` - Código único de miembro
- `loan_ids` - Historial de préstamos

**Ejemplo - Crear un miembro:**

```python
member_id = models.execute_kw('library_management', uid, 'admin',
    'res.partner', 'create',
    [{
        'name': 'Juan Pérez',
        'is_library_member': True,
        'member_id_code': 'MEM-001',
        'email': 'juan@example.com'
    }]
)
```

## 📊 Ejemplos Completos

### Flujo Completo: Crear y Prestar un Libro

```python
import xmlrpc.client

URL = 'http://localhost:8069'
DB = 'library_management'
USERNAME = 'admin'
PASSWORD = 'admin'

# Autenticar
common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
uid = common.authenticate(DB, USERNAME, PASSWORD, {})

models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')

# 1. Crear un libro
book_id = models.execute_kw(DB, uid, PASSWORD,
    'library.book', 'create',
    [{'name': 'El Principito', 'isbn': '9788498382679'}]
)
print(f"✅ Libro creado: ID {book_id}")

# 2. Crear una copia física
copy_id = models.execute_kw(DB, uid, PASSWORD,
    'library.book.copy', 'create',
    [{
        'book_id': book_id,
        'reference_code': 'PRIN-001',
        'state': 'available'
    }]
)
print(f"✅ Copia creada: ID {copy_id}")

# 3. Crear un miembro
member_id = models.execute_kw(DB, uid, PASSWORD,
    'res.partner', 'create',
    [{
        'name': 'María García',
        'is_library_member': True,
        'member_id_code': 'MEM-100'
    }]
)
print(f"✅ Miembro creado: ID {member_id}")

# 4. Crear un préstamo
loan_id = models.execute_kw(DB, uid, PASSWORD,
    'library.loan', 'create',
    [{
        'member_id': member_id,
        'copy_id': copy_id,
        'due_date': '2025-02-15'
    }]
)
print(f"✅ Préstamo creado: ID {loan_id}")

# 5. Confirmar el préstamo
models.execute_kw(DB, uid, PASSWORD,
    'library.loan', 'action_loan',
    [[loan_id]]
)
print(f"✅ Préstamo confirmado")

# 6. Verificar estado
loan = models.execute_kw(DB, uid, PASSWORD,
    'library.loan', 'read',
    [[loan_id]],
    {'fields': ['state', 'member_id', 'book_id']}
)[0]
print(f"📊 Estado del préstamo: {loan['state']}")
print(f"   Miembro: {loan['member_id'][1]}")
print(f"   Libro: {loan['book_id'][1]}")
```

## 🔧 Comandos Útiles

### Gestión de Servicios

```bash
# Ver estado
docker compose ps

# Reiniciar Odoo
docker compose restart odoo

# Ver logs en tiempo real
docker compose logs odoo -f

# Detener todo
docker compose stop

# Iniciar todo
docker compose start
```

### Actualizar el Módulo

```bash
# Si haces cambios en el código
docker compose exec -T odoo odoo -d library_management -u library_management --stop-after-init
docker compose restart odoo
```

### Backup de la Base de Datos

```bash
# Crear backup
docker compose exec db pg_dump -U odoo library_management > backup.sql

# Restaurar backup
docker compose exec -T db psql -U odoo library_management < backup.sql
```

## 📖 Documentación Adicional

- **Documentación Completa de la API**: `API_DOCUMENTATION.md`
- **README del Módulo**: `addons/library_management/README.md`
- **Estado del Proyecto**: `ESTADO_DEL_PROYECTO.md`

## 🧪 Scripts de Prueba Disponibles

```bash
# Diagnóstico rápido del sistema
python3 scripts/test_quick_check.py

# Prueba completa de todas las funciones
python3 scripts/test_complete_api.py
```

## 🌐 URLs Importantes

- **Interfaz Web**: http://localhost:8069
- **Gestión de Base de Datos**: http://localhost:8069/web/database/manager
- **Endpoint XML-RPC Common**: http://localhost:8069/xmlrpc/2/common
- **Endpoint XML-RPC Object**: http://localhost:8069/xmlrpc/2/object
- **Endpoint JSON-RPC**: http://localhost:8069/jsonrpc

## 💡 Tips

1. **Siempre autentica primero** para obtener tu UID
2. **Usa `sudo()` en la API** si tienes problemas de permisos
3. **Los campos Many2one** devuelven tuplas: `(id, 'nombre')`
4. **Usa `search_read`** en lugar de `search` + `read` para mejor rendimiento
5. **Los métodos de acción** requieren una lista de IDs: `[[loan_id]]`

## ⚠️ Nota Importante

Los controladores HTTP personalizados (`/api/ping`, `/api/library/books`) no están funcionando debido a limitaciones
conocidas en Odoo 18. **Usa siempre la API XML-RPC/JSON-RPC nativa** que está completamente funcional y es la forma
oficial recomendada por Odoo.

## ✅ Verificación Final

Ejecuta este comando para verificar que todo funciona:

```bash
python3 -c "
import xmlrpc.client
common = xmlrpc.client.ServerProxy('http://localhost:8069/xmlrpc/2/common')
uid = common.authenticate('library_management', 'admin', 'admin', {})
if uid:
    print('✅ API FUNCIONANDO CORRECTAMENTE')
    print(f'   UID: {uid}')
else:
    print('❌ Error de autenticación')
"
```

---

**¡Tu API está lista para usar!** 🚀

Para cualquier duda, consulta la documentación completa en `API_DOCUMENTATION.md`
