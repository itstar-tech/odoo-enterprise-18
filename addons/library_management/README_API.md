# 📚 API REST - Gestión de Biblioteca

API REST completa para integrar tu sistema de biblioteca con aplicaciones externas.

## 🔑 Autenticación

Todos los endpoints requieren una **API Key** que debe generarse desde Odoo:

1. Ve a **Ajustes → Usuarios y Compañías → Usuarios**
2. Selecciona un usuario con permisos
3. Ve a la pestaña **"API Access"**
4. Haz clic en **"Generar/Regenerar API Key"**
5. Copia la clave generada

La API Key se envía como parámetro en cada petición.

## 📖 Endpoints Disponibles

### **1. Health Check**
Verifica que la API está funcionando.

```bash
GET /api/library/health
```

**Ejemplo:**
```bash
curl http://localhost:8069/api/library/health
```

**Respuesta:**
```json
{
  "success": true,
  "message": "Library API is running",
  "version": "1.0",
  "timestamp": "2025-10-21T15:30:00"
}
```

---

### **2. Listar Libros**
Obtiene lista de libros con paginación y búsqueda.

```bash
GET /api/library/books?api_key=YOUR_KEY&limit=10&offset=0&search=Python
```

**Parámetros:**
- `api_key` (obligatorio): Tu clave de API
- `limit` (opcional): Número de resultados (default: 100)
- `offset` (opcional): Desplazamiento para paginación (default: 0)
- `search` (opcional): Buscar por título o autor

**Ejemplo:**
```bash
curl "http://localhost:8069/api/library/books?api_key=tu_api_key_aqui&limit=5"
```

**Respuesta:**
```json
{
  "success": true,
  "count": 5,
  "total": 50,
  "data": [
    {
      "id": 1,
      "title": "Python Programming",
      "isbn": "1234567890123",
      "authors": [
        {"id": 10, "name": "John Doe"}
      ],
      "sinopsis": "Learn Python from scratch",
      "availability": "available",
      "total_copies": 3,
      "available_copies": 2
    }
  ]
}
```

---

### **3. Obtener Detalle de un Libro**
Obtiene información completa de un libro específico.

```bash
GET /api/library/books/<book_id>?api_key=YOUR_KEY
```

**Ejemplo:**
```bash
curl "http://localhost:8069/api/library/books/1?api_key=tu_api_key_aqui"
```

**Respuesta:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "Python Programming",
    "isbn": "1234567890123",
    "authors": [{"id": 10, "name": "John Doe"}],
    "sinopsis": "Learn Python from scratch",
    "availability": "available",
    "copies": [
      {
        "id": 1,
        "reference_code": "PY-001",
        "state": "available",
        "location": "Estante A1"
      },
      {
        "id": 2,
        "reference_code": "PY-002",
        "state": "on_loan",
        "location": "Estante A1"
      }
    ]
  }
}
```

---

### **4. Crear un Nuevo Libro** ⭐
Crea un libro y opcionalmente sus copias.

```bash
POST /api/library/books
Content-Type: application/json
```

**Body JSON:**
```json
{
  "jsonrpc": "2.0",
  "params": {
    "api_key": "tu_api_key_aqui",
    "title": "Python Programming",
    "isbn": "1234567890123",
    "authors": [10, 15],
    "sinopsis": "Aprende Python desde cero",
    "copies": 3
  }
}
```

**Campos:**
- `api_key` (obligatorio): Tu clave de API
- `title` (obligatorio): Título del libro
- `isbn` (opcional): Código ISBN
- `authors` (opcional): Array de IDs de autores (res.partner)
- `sinopsis` (opcional): Descripción del libro
- `copies` (opcional): Número de copias físicas a crear

**Ejemplo con curl:**
```bash
curl -X POST http://localhost:8069/api/library/books \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "params": {
      "api_key": "tu_api_key_aqui",
      "title": "Python Programming",
      "isbn": "1234567890123",
      "copies": 2
    }
  }'
```

**Ejemplo con Python:**
```python
import requests

url = "http://localhost:8069/api/library/books"
payload = {
    "jsonrpc": "2.0",
    "params": {
        "api_key": "tu_api_key_aqui",
        "title": "Python Programming",
        "isbn": "1234567890123",
        "authors": [10],
        "sinopsis": "Un libro excelente sobre Python",
        "copies": 3
    }
}

response = requests.post(url, json=payload)
print(response.json())
```

**Ejemplo con JavaScript/Node.js:**
```javascript
const axios = require('axios');

const data = {
  jsonrpc: "2.0",
  params: {
    api_key: "tu_api_key_aqui",
    title: "Python Programming",
    isbn: "1234567890123",
    copies: 2
  }
};

axios.post('http://localhost:8069/api/library/books', data)
  .then(response => console.log(response.data))
  .catch(error => console.error(error));
```

**Respuesta:**
```json
{
  "jsonrpc": "2.0",
  "id": null,
  "result": {
    "success": true,
    "message": "Libro creado exitosamente",
    "data": {
      "id": 25,
      "title": "Python Programming",
      "isbn": "1234567890123",
      "copies_created": 3
    }
  }
}
```

---

### **5. Actualizar un Libro**
Actualiza información de un libro existente.

```bash
PUT /api/library/books/<book_id>
Content-Type: application/json
```

**Body JSON:**
```json
{
  "jsonrpc": "2.0",
  "params": {
    "api_key": "tu_api_key_aqui",
    "title": "Python Programming - 2da Edición",
    "sinopsis": "Versión actualizada del libro"
  }
}
```

**Ejemplo:**
```bash
curl -X PUT http://localhost:8069/api/library/books/1 \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "params": {
      "api_key": "tu_api_key_aqui",
      "title": "Nuevo Título"
    }
  }'
```

---

### **6. Listar Préstamos**
Obtiene lista de préstamos con filtros.

```bash
GET /api/library/loans?api_key=YOUR_KEY&state=active&member_id=5
```

**Parámetros:**
- `api_key` (obligatorio): Tu clave de API
- `state` (opcional): Filtrar por estado (draft, active, returned, overdue)
- `member_id` (opcional): Filtrar por ID de miembro
- `limit` (opcional): Número de resultados

**Ejemplo:**
```bash
curl "http://localhost:8069/api/library/loans?api_key=tu_api_key_aqui&state=active"
```

**Respuesta:**
```json
{
  "success": true,
  "count": 3,
  "data": [
    {
      "id": 15,
      "member": {
        "id": 5,
        "name": "Juan Pérez",
        "email": "juan@example.com"
      },
      "book": {
        "id": 1,
        "title": "Python Programming"
      },
      "copy_id": 2,
      "loan_date": "2025-10-15",
      "due_date": "2025-10-29",
      "return_date": null,
      "state": "active"
    }
  ]
}
```

---

### **7. Crear un Préstamo**
Crea un nuevo préstamo de libro.

```bash
POST /api/library/loans
Content-Type: application/json
```

**Body JSON:**
```json
{
  "jsonrpc": "2.0",
  "params": {
    "api_key": "tu_api_key_aqui",
    "member_id": 5,
    "copy_id": 2,
    "due_days": 14,
    "auto_confirm": true
  }
}
```

**Campos:**
- `api_key` (obligatorio): Tu clave de API
- `member_id` (obligatorio): ID del miembro que presta
- `copy_id` (obligatorio): ID de la copia física del libro
- `due_days` (opcional): Días hasta vencimiento (default: 14)
- `auto_confirm` (opcional): Confirmar préstamo automáticamente (default: false)

**Ejemplo:**
```python
import requests

url = "http://localhost:8069/api/library/loans"
payload = {
    "jsonrpc": "2.0",
    "params": {
        "api_key": "tu_api_key_aqui",
        "member_id": 5,
        "copy_id": 2,
        "due_days": 21,
        "auto_confirm": True
    }
}

response = requests.post(url, json=payload)
print(response.json())
```

---

### **8. Devolver un Préstamo**
Registra la devolución de un libro.

```bash
POST /api/library/loans/<loan_id>/return
Content-Type: application/json
```

**Body JSON:**
```json
{
  "jsonrpc": "2.0",
  "params": {
    "api_key": "tu_api_key_aqui"
  }
}
```

**Ejemplo:**
```bash
curl -X POST http://localhost:8069/api/library/loans/15/return \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "params": {
      "api_key": "tu_api_key_aqui"
    }
  }'
```

---

### **9. Listar Miembros**
Obtiene lista de miembros de la biblioteca.

```bash
GET /api/library/members?api_key=YOUR_KEY&search=juan
```

**Ejemplo:**
```bash
curl "http://localhost:8069/api/library/members?api_key=tu_api_key_aqui"
```

**Respuesta:**
```json
{
  "success": true,
  "count": 2,
  "data": [
    {
      "id": 5,
      "name": "Juan Pérez",
      "email": "juan@example.com",
      "phone": "+1234567890",
      "active_loans": 2
    }
  ]
}
```

---

## 🔒 Seguridad

- ⚠️ **Nunca compartas tu API Key**
- 🔄 Regenera tu API Key si sospechas que ha sido comprometida
- 🔐 Usa HTTPS en producción
- 👥 Crea usuarios específicos para integraciones API con permisos limitados

---

## 🐛 Manejo de Errores

Todas las respuestas de error siguen este formato:

```json
{
  "success": false,
  "error": "Descripción del error"
}
```

**Códigos de estado HTTP:**
- `200`: Éxito
- `400`: Error de validación o datos incorrectos
- `401`: API Key inválida o faltante
- `404`: Recurso no encontrado
- `500`: Error interno del servidor

---

## 📝 Ejemplo Completo: Aplicación Python

```python
import requests

class LibraryAPI:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key
    
    def create_book(self, title, isbn=None, copies=1):
        """Crea un nuevo libro"""
        url = f"{self.base_url}/api/library/books"
        payload = {
            "jsonrpc": "2.0",
            "params": {
                "api_key": self.api_key,
                "title": title,
                "isbn": isbn,
                "copies": copies
            }
        }
        response = requests.post(url, json=payload)
        return response.json()
    
    def list_books(self, search=None, limit=10):
        """Lista libros"""
        url = f"{self.base_url}/api/library/books"
        params = {
            "api_key": self.api_key,
            "limit": limit
        }
        if search:
            params["search"] = search
        
        response = requests.get(url, params=params)
        return response.json()
    
    def create_loan(self, member_id, copy_id, due_days=14):
        """Crea un préstamo"""
        url = f"{self.base_url}/api/library/loans"
        payload = {
            "jsonrpc": "2.0",
            "params": {
                "api_key": self.api_key,
                "member_id": member_id,
                "copy_id": copy_id,
                "due_days": due_days,
                "auto_confirm": True
            }
        }
        response = requests.post(url, json=payload)
        return response.json()

# Uso
api = LibraryAPI("http://localhost:8069", "tu_api_key_aqui")

# Crear libro
result = api.create_book("Python Programming", "1234567890", copies=3)
print(f"Libro creado: {result}")

# Listar libros
books = api.list_books(search="Python")
print(f"Libros encontrados: {books}")

# Crear préstamo
loan = api.create_loan(member_id=5, copy_id=2, due_days=21)
print(f"Préstamo creado: {loan}")
```

---

## 🎯 Casos de Uso

1. **Aplicación móvil**: Consultar disponibilidad y crear préstamos
2. **Sistema de kiosco**: Auto-préstamo para usuarios
3. **Integración con sistema escolar**: Sincronizar estudiantes y préstamos
4. **Dashboard externo**: Visualizar estadísticas en tiempo real
5. **Notificaciones automáticas**: Sistema externo que envía recordatorios

---

## 📞 Soporte

Para más información o soporte, contacta con el administrador del sistema.
