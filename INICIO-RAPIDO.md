# ✅ Instalación Completada - Odoo 18 Enterprise

## 🎉 Estado del Sistema

✅ **PostgreSQL 16**: Corriendo en puerto **5432**  
✅ **Odoo 18.0**: Corriendo en puerto **8069**  
✅ **Docker Compose**: Configurado y funcionando

---

## 🌐 Acceso a Odoo

### URL Principal
**http://localhost:8069**

### Credenciales por Defecto
- **Master Password**: `admin` (para crear/gestionar bases de datos)
- **Base de datos**: `odoo` (se crea en el primer acceso)

---

## 🚀 Primer Uso

### 1. Acceder a Odoo
```bash
# Opción 1: En tu navegador
http://localhost:8069

# Opción 2: Si estás en Codespaces, usa la URL pública que GitHub te proporciona
```

### 2. Crear Base de Datos
Al acceder por primera vez, verás un formulario para crear la base de datos:

1. **Master Password**: `admin`
2. **Database Name**: `odoo`
3. **Email**: tu_email@ejemplo.com
4. **Password**: Una contraseña segura
5. **Language**: Español / Spanish
6. **Country**: México / Tu país
7. **Demo data**: ✅ Marcar si quieres datos de prueba

---

## 📊 Comandos Útiles

### Ver logs en tiempo real
```bash
docker-compose logs -f odoo
```

### Reiniciar Odoo
```bash
docker-compose restart odoo
```

### Detener todo
```bash
docker-compose stop
```

### Iniciar todo
```bash
docker-compose start
```

### Reiniciar desde cero (⚠️ ELIMINA TODOS LOS DATOS)
```bash
docker-compose down -v
docker-compose up -d
```

### Acceder a la terminal de Odoo
```bash
docker-compose exec odoo bash
```

### Acceder a PostgreSQL
```bash
docker-compose exec db psql -U odoo -d odoo
```

---

## 🔧 Configuración Actual

### Archivos Creados
- ✅ `docker-compose.yml` - Configuración de servicios
- ✅ `.env` - Variables de entorno
- ✅ `README-DOCKER.md` - Documentación completa
- ✅ `INICIO-RAPIDO.md` - Este archivo

### Puertos
- **Odoo**: 8069 → http://localhost:8069
- **PostgreSQL**: 5433 (internamente 5432)

### Volúmenes
- `pgdata` - Datos de PostgreSQL
- `odoo-data` - Archivos de Odoo

### Carpetas Montadas
- `./addons` → `/mnt/extra-addons` (módulos personalizados)
- `./odoo` → `/usr/lib/python3/dist-packages/odoo` (código fuente)

---

## 🛠️ Desarrollo

### Agregar módulos personalizados
1. Coloca tus módulos en la carpeta `addons/`
2. Reinicia Odoo: `docker-compose restart odoo`
3. En Odoo, ve a Aplicaciones → Actualizar lista de aplicaciones

### Instalar dependencias Python adicionales
```bash
docker-compose exec odoo pip install nombre-paquete
```

### Modo desarrollo
El sistema ya está en modo desarrollo (`--dev=all`), que incluye:
- ✅ Recarga automática de código
- ✅ Logs detallados
- ✅ Depuración activada

---

## 🐛 Solución de Problemas

### Odoo no carga
```bash
# Ver los logs
docker-compose logs odoo

# Reiniciar
docker-compose restart odoo
```

### Base de datos no se conecta
```bash
# Verificar que PostgreSQL esté corriendo
docker-compose ps

# Ver logs de PostgreSQL
docker-compose logs db
```

### Puerto ocupado
Si el puerto 8069 está ocupado, modifica `docker-compose.yml`:
```yaml
ports:
  - "8070:8069"  # Usa 8070 en lugar de 8069
```

### Resetear completamente
```bash
# ⚠️ CUIDADO: Esto elimina TODOS los datos
docker-compose down -v
docker-compose up -d
```

---

## 📦 Backup y Restauración

### Hacer backup de la base de datos
```bash
docker-compose exec db pg_dump -U odoo odoo > backup_$(date +%Y%m%d_%H%M%S).sql
```

### Restaurar backup
```bash
docker-compose exec -T db psql -U odoo odoo < backup_20251014_123456.sql
```

---

## 🔐 Seguridad

### ⚠️ Antes de ir a producción:

1. Cambia las contraseñas en `.env`:
```env
POSTGRES_PASSWORD=tu_contraseña_super_segura
```

2. Cambia el master password de Odoo
3. Usa HTTPS con certificado SSL
4. Configura firewall
5. Implementa backups automáticos

---

## 📚 Recursos

- **Documentación Odoo 18**: https://www.odoo.com/documentation/18.0/
- **Documentación Developer**: https://www.odoo.com/documentation/18.0/developer.html
- **README Completo**: Ver `README-DOCKER.md`
- **Requirements**: Ver `requirements.txt`

---

## ✨ Próximos Pasos

1. [ ] Accede a http://localhost:8069
2. [ ] Crea tu primera base de datos
3. [ ] Instala los módulos que necesites
4. [ ] Personaliza Odoo según tus necesidades
5. [ ] Desarrolla tus propios módulos en `addons/`

---

## 💡 Tips

- Los cambios en módulos se detectan automáticamente (modo `--dev`)
- Puedes tener múltiples bases de datos en la misma instancia
- Los datos persisten entre reinicios (volúmenes Docker)
- Para desarrollo rápido, usa datos demo

---

**🎊 ¡Tu entorno de desarrollo Odoo está listo para usar!**

Para más detalles, consulta `README-DOCKER.md`
