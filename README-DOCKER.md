# 🚀 Odoo 18 Enterprise - Guía de Instalación con Docker

## 📋 Prerrequisitos

- Docker instalado
- Docker Compose instalado
- Al menos 4GB de RAM disponible

## 🏗️ Estructura del Proyecto

```
odoo-enterprise-18/
├── docker-compose.yml    # Configuración de contenedores
├── .env                  # Variables de entorno
├── addons/              # Módulos adicionales
├── odoo/                # Código fuente de Odoo
└── requirements.txt     # Dependencias Python
```

## ⚙️ Configuración

### 1. Variables de Entorno

El archivo `.env` contiene:
```env
POSTGRES_DB=odoo
POSTGRES_USER=odoo
POSTGRES_PASSWORD=odoo
ODOO_VERSION=18.0
```

**⚠️ Importante:** Cambia las contraseñas en producción.

## 🚀 Iniciar el Proyecto

### Opción 1: Inicio Rápido

```bash
# Levantar los servicios
docker-compose up -d

# Ver los logs
docker-compose logs -f odoo
```

### Opción 2: Reconstruir desde cero

```bash
# Detener y eliminar contenedores existentes
docker-compose down -v

# Reconstruir y levantar
docker-compose up -d --build

# Ver logs en tiempo real
docker-compose logs -f
```

## 📊 Acceder a Odoo

Una vez que los servicios estén ejecutándose:

1. **URL de Odoo:** http://localhost:8069
2. **Base de datos:** `odoo` (se crea automáticamente)
3. **Usuario master password:** `admin` (por defecto)

### Primera Configuración

1. Abre http://localhost:8069
2. Completa el formulario de creación de base de datos:
   - **Master Password:** admin
   - **Database Name:** odoo
   - **Email:** tu@email.com
   - **Password:** tu_contraseña_segura
   - **Language:** Español
   - **Country:** Tu país

## 🛠️ Comandos Útiles

### Ver logs
```bash
# Todos los servicios
docker-compose logs -f

# Solo Odoo
docker-compose logs -f odoo

# Solo PostgreSQL
docker-compose logs -f db
```

### Reiniciar servicios
```bash
# Reiniciar todos
docker-compose restart

# Reiniciar solo Odoo
docker-compose restart odoo
```

### Detener servicios
```bash
# Detener (mantiene datos)
docker-compose stop

# Detener y eliminar contenedores (mantiene volúmenes)
docker-compose down

# Detener y eliminar TODO (incluyendo datos)
docker-compose down -v
```

### Acceder a la shell de Odoo
```bash
docker-compose exec odoo bash
```

### Acceder a PostgreSQL
```bash
# Conectar a la base de datos
docker-compose exec db psql -U odoo -d odoo

# Listar bases de datos
docker-compose exec db psql -U odoo -l
```

### Ejecutar comandos de Odoo
```bash
# Actualizar módulos
docker-compose exec odoo odoo shell -d odoo

# Modo scaffold (crear nuevo módulo)
docker-compose exec odoo odoo scaffold mi_modulo /mnt/extra-addons/
```

## 🔧 Desarrollo

### Instalar dependencias adicionales en el contenedor

```bash
docker-compose exec odoo pip install nombre_paquete
```

### Modo desarrollo

El `docker-compose.yml` ya incluye `--dev=all` que activa:
- Recarga automática de código
- Logs detallados
- Modo debug

### Agregar módulos personalizados

1. Coloca tus módulos en la carpeta `addons/`
2. Reinicia Odoo: `docker-compose restart odoo`
3. Actualiza la lista de aplicaciones en Odoo

## 🐛 Solución de Problemas

### Problema: Puerto 5432 o 8069 ya están en uso

```bash
# Ver qué proceso usa el puerto
sudo lsof -i :8069
sudo lsof -i :5432

# Cambiar puertos en docker-compose.yml
# Por ejemplo: "8070:8069" en lugar de "8069:8069"
```

### Problema: Odoo no se conecta a PostgreSQL

```bash
# Verificar que la base de datos esté lista
docker-compose logs db

# Reiniciar servicios
docker-compose restart
```

### Problema: Cambios en código no se reflejan

```bash
# Reiniciar Odoo (modo dev debería detectar cambios)
docker-compose restart odoo

# Si persiste, reconstruir
docker-compose up -d --build
```

### Resetear completamente

```bash
# CUIDADO: Esto elimina TODOS los datos
docker-compose down -v
docker-compose up -d
```

## 📦 Volúmenes de Datos

Los datos se almacenan en volúmenes Docker:
- `pgdata`: Datos de PostgreSQL
- `odoo-data`: Archivos de Odoo

Para hacer backup:
```bash
# Backup PostgreSQL
docker-compose exec db pg_dump -U odoo odoo > backup.sql

# Restaurar
docker-compose exec -T db psql -U odoo odoo < backup.sql
```

## 🔐 Seguridad (Producción)

Para producción, modifica:

1. **Contraseñas fuertes** en `.env`
2. **Admin password** de Odoo
3. **Exponer solo puertos necesarios**
4. **Variables de entorno secretas**
5. **Usar volúmenes con backup**

## 📚 Recursos Adicionales

- [Documentación Odoo 18](https://www.odoo.com/documentation/18.0/)
- [Odoo Developer Documentation](https://www.odoo.com/documentation/18.0/developer.html)
- [Docker Compose Docs](https://docs.docker.com/compose/)

## ✅ Checklist de Inicio

- [ ] Docker y Docker Compose instalados
- [ ] Archivo `.env` configurado
- [ ] Ejecutar `docker-compose up -d`
- [ ] Verificar logs: `docker-compose logs -f`
- [ ] Acceder a http://localhost:8069
- [ ] Crear base de datos
- [ ] Instalar módulos necesarios

---

**🎉 ¡Tu entorno de desarrollo Odoo está listo!**
