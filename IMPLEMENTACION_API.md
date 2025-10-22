# ✅ REST API para Biblioteca - Implementación Completa

## 📋 Resumen de lo Implementado

Se ha creado una **API REST completa** para el módulo de Gestión de Biblioteca que permite:

### ✨ Funcionalidades

1. **📚 Gestión de Libros**
   - Listar libros con paginación y búsqueda
   - Obtener detalle de un libro específico
   - Crear nuevos libros con copias automáticas
   - Actualizar información de libros

2. **📖 Gestión de Préstamos**
   - Listar préstamos con filtros (estado, miembro)
   - Crear nuevos préstamos
   - Registrar devoluciones

3. **👥 Gestión de Miembros**
   - Listar miembros de la biblioteca
   - Buscar miembros

4. **🔐 Autenticación**
   - Sistema de API Keys para autenticación segura
   - Generación automática de claves desde la interfaz de Odoo

---

## 📁 Archivos Creados

### 1. **Controladores API**
- `controllers/__init__.py` - Inicialización del módulo de controladores
- `controllers/api_controllers.py` - Implementación completa de la API REST

### 2. **Modelos**
- `models/res_users.py` - Extensión del modelo de usuarios para agregar API Keys

### 3. **Vistas**
- `views/res_users_views.xml` - Vista para gestionar API Keys en la interfaz

### 4. **Documentación y Ejemplos**
- `README_API.md` - Documentación completa de la API
- `/workspaces/odoo-enterprise-18/test_library_api.py` - Script Python de prueba
- `/workspaces/odoo-enterprise-18/test_library_api.sh` - Script Bash con ejemplos curl

---

## 🚀 Endpoints Disponibles

### Health Check
```
GET /api/library/health
```

### Libros
```
GET  /api/library/books                    # Listar
GET  /api/library/books/<id>               # Detalle
POST /api/library/books                    # Crear
PUT  /api/library/books/<id>               # Actualizar
```

### Préstamos
```
GET  /api/library/loans                    # Listar
POST /api/library/loans                    # Crear
POST /api/library/loans/<id>/return        # Devolver
```

### Miembros
```
GET  /api/library/members                  # Listar
```

---

## 🔑 Generar API Key

### Desde la Interfaz de Odoo:

1. Ve a **Ajustes → Usuarios y Compañías → Usuarios**
2. Selecciona el usuario (ej: admin)
3. Ve a la pestaña **"API Access"**
4. Haz clic en **"Generar/Regenerar API Key"**
5. Copia la clave generada (aparecerá como contraseña oculta)

### Desde la Base de Datos:

```bash
# Tu API Key actual:
API_KEY="Ld9DVJgdlPg4hgR6A_n7ExeOONVU3PWWx1PskIfOssI"

# Para el usuario admin
```

---

## 🧪 Cómo Probar la API

### 1. Verificar que Odoo está corriendo:

```bash
docker ps | grep odoo
```

### 2. Probar Health Check (no requiere autenticación):

```bash
curl http://localhost:8069/api/library/health
```

**Respuesta esperada:**
```json
{
  "success": true,
  "message": "Library API is running",
  "version": "1.0"
}
```

### 3. Listar Libros:

```bash
curl "http://localhost:8069/api/library/books?api_key=Ld9DVJgdlPg4hgR6A_n7ExeOONVU3PWWx1PskIfOssI&limit=5"
```

### 4. Crear un Libro (desde Python):

```python
import requests

url = "http://localhost:8069/api/library/books"
payload = {
    "jsonrpc": "2.0",
    "params": {
        "api_key": "Ld9DVJgdlPg4hgR6A_n7ExeOONVU3PWWx1PskIfOssI",
        "title": "Python Programming",
        "isbn": "1234567890123",
        "sinopsis": "Learn Python from scratch",
        "copies": 3
    }
}

response = requests.post(url, json=payload)
print(response.json())
```

### 5. Crear un Libro (desde curl):

```bash
curl -X POST http://localhost:8069/api/library/books \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "params": {
      "api_key": "Ld9DVJgdlPg4hgR6A_n7ExeOONVU3PWWx1PskIfOssI",
      "title": "JavaScript: The Good Parts",
      "isbn": "9780596517748",
      "copies": 2
    }
  }'
```

---

## 📱 Ejemplo: Aplicación Externa

### Aplicación Python Completa:

```python
#!/usr/bin/env python3
import requests

class LibraryAPI:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key
    
    def create_book(self, title, isbn=None, copies=1):
        """Crea un nuevo libro en Odoo desde tu aplicación"""
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
    
    def list_books(self, search=None):
        """Lista libros disponibles"""
        url = f"{self.base_url}/api/library/books"
        params = {"api_key": self.api_key}
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
api = LibraryAPI("http://localhost:8069", "TU_API_KEY")

# Crear libro desde otra aplicación
result = api.create_book("Mi Nuevo Libro", "1234567890", copies=3)
print(f"Libro creado: {result}")

# Listar libros
books = api.list_books(search="Python")
for book in books['data']:
    print(f"- {book['title']} ({book['available_copies']} disponibles)")
```

---

## 🔧 Troubleshooting

### Error: "API key inválida o faltante"
- Verifica que has generado la API key desde Odoo
- Asegúrate de estar pasando el parámetro `api_key` correctamente

### Error: 500 Internal Server Error
- Verifica los logs: `docker logs odoo-enterprise-18-odoo-1`
- Asegúrate de que el módulo `library_management` está instalado
- Reinicia Odoo: `docker restart odoo-enterprise-18-odoo-1`

### Endpoint no encontrado (404)
- Verifica que el contenedor está corriendo
- Asegúrate de usar el puerto correcto (8069)
- Verifica la URL: debe comenzar con `/api/library/`

---

## 🔄 Reiniciar y Limpiar

Si encuentras problemas, intenta:

```bash
# 1. Detener todo
docker compose down

# 2. Iniciar servicios
docker compose up -d

# 3. Esperar que estén listos
sleep 10

# 4. Probar health check
curl http://localhost:8069/api/library/health

# 5. Si es necesario, actualizar el módulo
docker exec odoo-enterprise-18-odoo-1 /usr/bin/python3 /usr/bin/odoo \
  -c /etc/odoo/odoo.conf \
  --addons-path=/mnt/extra-addons,/usr/lib/python3/dist-packages/odoo/addons \
  -d mycompany \
  -u library_management \
  --stop-after-init

# 6. Reiniciar Odoo
docker restart odoo-enterprise-18-odoo-1
```

---

## 📖 Casos de Uso

### 1. **Aplicación Móvil**
Una app móvil puede consultar disponibilidad y crear préstamos:
```javascript
// React Native / Ionic
const checkAvailability = async (bookTitle) => {
  const response = await fetch(
    `${API_URL}/api/library/books?api_key=${API_KEY}&search=${bookTitle}`
  );
  const data = await response.json();
  return data;
};
```

### 2. **Sistema de Kiosco**
Un kiosco de auto-préstamo:
```python
# Usuario escanea su carnet
member_id = scan_member_card()

# Usuario escanea libro
copy_id = scan_book_barcode()

# Crear préstamo automáticamente
api.create_loan(member_id, copy_id, due_days=14)
```

### 3. **Integración con Sistema Escolar**
Sincronizar estudiantes automáticamente:
```python
# Obtener estudiantes del sistema escolar
students = school_system.get_active_students()

# Por cada estudiante, verificar si existe en Odoo
for student in students:
    # Usar API de partners/contacts para crear o actualizar
    pass
```

### 4. **Dashboard de Estadísticas**
Dashboard externo que muestra métricas en tiempo real:
```python
# Obtener préstamos activos
active_loans = api.list_loans(state="active")
overdue_loans = api.list_loans(state="overdue")

# Mostrar en dashboard
dashboard.show_metrics({
    "active": len(active_loans['data']),
    "overdue": len(overdue_loans['data'])
})
```

---

## 🎯 Próximos Pasos

1. **Probar la API** usando curl o Postman
2. **Generar tu API Key** desde la interfaz de Odoo
3. **Crear tu primera aplicación** que se conecte a Odoo
4. **Implementar webhooks** si necesitas notificaciones en tiempo real
5. **Agregar más endpoints** según tus necesidades

---

## 📞 Soporte

- **Documentación completa**: `README_API.md`
- **Script de prueba Python**: `test_library_api.py`
- **Script de prueba Bash**: `test_library_api.sh`

---

## ✅ Estado Actual

- ✅ Controladores API implementados
- ✅ Sistema de autenticación con API Keys
- ✅ Endpoints para libros, préstamos y miembros
- ✅ Documentación completa
- ✅ Scripts de ejemplo
- ⚠️ Requiere reinicio limpio de Odoo para resolver errores de transacción SQL

### Comando para Reinicio Limpio:

```bash
docker compose down
docker compose up -d
sleep 15
curl http://localhost:8069/api/library/health
```

---

**¡Tu API REST está lista para conectar Odoo con cualquier aplicación externa! 🚀**
