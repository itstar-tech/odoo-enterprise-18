# 🚀 Configuración Completa de Odoo 18 Enterprise

## ✅ Estado Actual

Tu instalación de Odoo 18 está completamente configurada con:

### 📦 Módulos Disponibles:
- ✅ **Módulos Community** (base de Odoo) - ~100+ módulos
- ✅ **Módulos Enterprise** - ~500+ módulos 
- ✅ **Módulos Personalizados** - library_management y otros

### 🗂️ Estructura de Carpetas:

```
odoo-enterprise-18/
├── addons/                    # Todos los módulos (Community + Enterprise + Personalizados)
│   ├── account/              # Módulos de contabilidad
│   ├── hr_*/                 # Módulos de recursos humanos
│   ├── sale_*/               # Módulos de ventas
│   ├── library_management/   # Tu módulo personalizado ✨
│   └── ... (598 módulos más)
├── odoo/                      # Código fuente de Odoo (para referencia)
├── config/
│   └── odoo.conf             # Configuración de Odoo
├── docker-compose.yml         # Configuración de Docker
└── check-modules.sh          # Script de utilidades
```

---

## 🐳 Docker Compose - Configuración

### Servicios Configurados:

1. **PostgreSQL 16**
   - Puerto: 5433 (para evitar conflictos)
   - Usuario: odoo / odoo
   - Base de datos: odoo

2. **Odoo 18.0**
   - Puerto: 8069
   - Modo desarrollo: Activado
   - Addons montados: TODOS (community + enterprise + personalizados)

### Volúmenes Montados:

```yaml
volumes:
  - ./addons:/mnt/extra-addons              # TODOS los addons
  - ./odoo:/mnt/odoo-src                    # Código fuente
  - odoo-data:/var/lib/odoo                 # Datos persistentes
  - ./config:/etc/odoo                      # Configuración
```

### Rutas de Addons (sin conflictos):

```
addons_path = /usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons
```

**Orden de búsqueda:**
1. Primero: `/usr/lib/python3/dist-packages/odoo/addons` (base de Odoo)
2. Segundo: `/mnt/extra-addons` (tus módulos tienen prioridad)

---

## 🛠️ Comandos Útiles

### Gestión de Servicios:

```bash
# Iniciar servicios
docker-compose up -d

# Detener servicios
docker-compose stop

# Ver logs
docker-compose logs -f odoo

# Reiniciar Odoo
docker-compose restart odoo

# Detener y eliminar (mantiene datos)
docker-compose down

# Resetear TODO (⚠️ elimina datos)
docker-compose down -v
```

### Verificar Módulos:

```bash
# Ejecutar script de verificación
./check-modules.sh

# Ver módulos montados manualmente
docker-compose exec odoo ls /mnt/extra-addons | wc -l

# Ver configuración
docker-compose exec odoo cat /etc/odoo/odoo.conf
```

### Actualizar Módulos:

```bash
# Actualizar lista de módulos
docker-compose exec odoo odoo -d odoo --stop-after-init --update=all --db_host=db --db_user=odoo --db_password=odoo

# Instalar un módulo específico
docker-compose exec odoo odoo -d odoo --stop-after-init -i nombre_modulo --db_host=db --db_user=odoo --db_password=odoo

# Actualizar un módulo específico
docker-compose exec odoo odoo -d odoo --stop-after-init -u nombre_modulo --db_host=db --db_user=odoo --db_password=odoo
```

---

## 🌐 Acceso a Odoo

### URL Principal:
**http://localhost:8069**

O si estás en Codespaces:
**https://tu-codespace.github.dev:8069**

### Credenciales Iniciales:
- **Usuario:** admin
- **Contraseña:** admin

---

## 📚 Módulos Disponibles

### Módulos Community (Incluidos en Odoo base):
- Contabilidad básica
- CRM
- Ventas
- Compras
- Inventario
- Sitio web
- Blog
- Eventos
- Y más...

### Módulos Enterprise (En tu carpeta addons):
- **Contabilidad Avanzada:** account_*
- **Recursos Humanos:** hr_*, hr_payroll_*
- **Ventas Avanzadas:** sale_*, pos_*
- **Proyectos:** project_*
- **Marketing:** marketing_*, social_*
- **eCommerce:** website_sale_*
- **Fabricación:** mrp_*
- **Y muchos más...**

### Módulos Personalizados:
- ✨ **library_management** - Gestión de Biblioteca (instalado)
- Puedes crear más módulos en `/addons/`

---

## 🔧 Configuración Avanzada

### Archivo: `/config/odoo.conf`

```ini
[options]
# Base de datos
db_host = db
db_port = 5432
db_user = odoo
db_password = odoo

# Rutas de addons
addons_path = /usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons

# Servidor
http_port = 8069
workers = 0

# Desarrollo
dev_mode = reload,qweb,werkzeug,xml

# Seguridad
admin_passwd = admin  # ⚠️ Cambia esto en producción
```

### Modificar Configuración:

1. Edita `/config/odoo.conf`
2. Reinicia Odoo: `docker-compose restart odoo`

---

## 🆕 Crear Módulo Personalizado

### 1. Crear estructura:

```bash
cd addons
mkdir mi_nuevo_modulo
cd mi_nuevo_modulo
```

### 2. Crear archivos básicos:

```bash
touch __init__.py __manifest__.py
mkdir models views security
```

### 3. Actualizar lista y instalar:

```bash
# Desde Odoo UI: Aplicaciones → Actualizar lista de aplicaciones
# O desde terminal:
docker-compose restart odoo
```

---

## 🔍 Verificación de Conflictos

### ¿Cómo evitar conflictos?

1. **Nombres únicos:** Los módulos en `/mnt/extra-addons` tienen prioridad
2. **No duplicar:** Si hay un módulo con el mismo nombre en ambas rutas, se usa el de `/mnt/extra-addons`
3. **Dependencias:** Asegúrate de que las dependencias estén disponibles

### Verificar si hay conflictos:

```bash
# Ver módulos duplicados
docker-compose exec odoo bash -c "
  ls /usr/lib/python3/dist-packages/odoo/addons > /tmp/base.txt
  ls /mnt/extra-addons > /tmp/extra.txt
  comm -12 <(sort /tmp/base.txt) <(sort /tmp/extra.txt)
"
```

---

## 🐛 Solución de Problemas

### Problema: Módulo no aparece

```bash
# Solución 1: Actualizar lista
docker-compose restart odoo
# En Odoo: Aplicaciones → Actualizar lista

# Solución 2: Verificar que esté montado
docker-compose exec odoo ls /mnt/extra-addons/nombre_modulo
```

### Problema: Error al instalar módulo

```bash
# Ver logs detallados
docker-compose logs odoo | tail -100

# Verificar sintaxis del manifest
docker-compose exec odoo python3 -m py_compile /mnt/extra-addons/nombre_modulo/__manifest__.py
```

### Problema: Base de datos corrupta

```bash
# Resetear base de datos
docker-compose down -v
docker-compose up -d
```

---

## 📊 Información del Sistema

### Versión de Odoo:
```bash
docker-compose exec odoo odoo --version
# Resultado: Odoo Server 18.0
```

### Número de módulos:
```bash
./check-modules.sh
```

### Espacio en disco:
```bash
docker-compose exec odoo df -h /var/lib/odoo
```

---

## 🎯 Próximos Pasos

1. ✅ Accede a Odoo: http://localhost:8069
2. ✅ Inicia sesión con admin/admin
3. ✅ Ve a **Aplicaciones**
4. ✅ Click en **Actualizar lista de aplicaciones**
5. ✅ Busca e instala los módulos que necesites
6. ✅ Desarrolla tus propios módulos en `/addons/`

---

## 📞 Comandos Rápidos

```bash
# Iniciar
docker-compose up -d

# Ver logs
docker-compose logs -f odoo

# Verificar módulos
./check-modules.sh

# Reiniciar
docker-compose restart odoo

# Acceder
open http://localhost:8069
```

---

## ✨ Características Especiales

### ✅ Modo Desarrollo Activado
- Recarga automática de código
- Logs detallados
- Debugging activado

### ✅ Todos los Addons Montados
- Community
- Enterprise
- Personalizados

### ✅ Sin Conflictos
- Rutas bien definidas
- Prioridad correcta
- Aislamiento adecuado

---

**🎉 Tu entorno Odoo 18 Enterprise está completamente configurado y listo para usar!**
