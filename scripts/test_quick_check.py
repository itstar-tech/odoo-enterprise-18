#!/usr/bin/env python3
"""
Script de diagnóstico rápido para la API de Odoo
"""
import xmlrpc.client
import sys

URL = 'http://localhost:8069'

print("=" * 70)
print("DIAGNÓSTICO RÁPIDO DE LA API DE ODOO")
print("=" * 70)
print()

print("🔍 Verificando conectividad...")
print(f"   URL: {URL}")
print()

try:
    common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')

    print("✅ Conexión establecida con el servidor Odoo")
    print()

    print("📊 Información del servidor:")
    version_info = common.version()
    print(f"   Versión: {version_info.get('server_version', 'N/A')}")
    print(f"   Serie: {version_info.get('server_serie', 'N/A')}")
    print(f"   Protocolo: {version_info.get('protocol_version', 'N/A')}")
    print()

    print("=" * 70)
    print("PRUEBA DE AUTENTICACIÓN")
    print("=" * 70)
    print()

    databases = ['odoo', 'library_management', 'TU_BD']
    credentials = [
        ('admin', 'admin'),
        ('admin', ''),
        ('admin', 'password'),
    ]

    authenticated = False

    for db in databases:
        if authenticated:
            break
        print(f"🔐 Probando base de datos: {db}")
        for username, password in credentials:
            try:
                uid = common.authenticate(db, username, password, {})
                if uid:
                    print(f"   ✅ ÉXITO con usuario '{username}'")
                    print(f"      UID: {uid}")
                    print(f"      Base de datos: {db}")
                    authenticated = True

                    print()
                    print("=" * 70)
                    print("PROBANDO ACCESO A MÓDULO")
                    print("=" * 70)
                    print()

                    models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')

                    try:
                        count = models.execute_kw(db, uid, password,
                                                  'library.book', 'search_count', [[]]
                                                  )
                        print(f"✅ Módulo 'library_management' INSTALADO Y FUNCIONAL")
                        print(f"   Total de libros en el sistema: {count}")
                        print()

                        books = models.execute_kw(db, uid, password,
                                                  'library.book', 'search_read',
                                                  [[]],
                                                  {'fields': ['id', 'name'], 'limit': 3}
                                                  )

                        if books:
                            print(f"   Primeros libros:")
                            for book in books:
                                print(f"      • {book['name']} (ID: {book['id']})")

                        print()
                        print("=" * 70)
                        print("✅ TODO ESTÁ FUNCIONANDO CORRECTAMENTE")
                        print("=" * 70)
                        print()
                        print(f"🎉 Puedes usar estas credenciales:")
                        print(f"   URL: {URL}")
                        print(f"   Base de datos: {db}")
                        print(f"   Usuario: {username}")
                        print(f"   Contraseña: {password if password else '(vacía)'}")
                        print()
                        print(f"📚 Ver documentación completa en: API_DOCUMENTATION.md")
                        print(f"🌐 Interfaz web: {URL}")

                    except Exception as e:
                        print(f"⚠️  Módulo no encontrado o no instalado: {e}")
                        print(
                            f"   Ejecuta: docker compose exec -T odoo odoo -d {db} -u library_management --stop-after-init")

                    break
            except Exception as e:
                continue

        if not authenticated:
            print(f"   ❌ No se pudo autenticar en '{db}'")
        print()

    if not authenticated:
        print("=" * 70)
        print("⚠️  NO SE PUDO AUTENTICAR")
        print("=" * 70)
        print()
        print("Posibles soluciones:")
        print("  1. Accede a la interfaz web: http://localhost:8069")
        print("  2. Crea una base de datos y un usuario administrador")
        print("  3. Instala el módulo 'library_management'")
        print("  4. Actualiza este script con las credenciales correctas")
        print()
        print("Comando para crear base de datos:")
        print("  Accede a: http://localhost:8069/web/database/manager")

except Exception as e:
    print(f"❌ Error de conexión: {e}")
    print()
    print("Troubleshooting:")
    print("  1. Verifica que Odoo esté corriendo:")
    print("     docker compose ps")
    print()
    print("  2. Verifica los logs:")
    print("     docker compose logs odoo --tail=50")
    print()
    print("  3. Reinicia Odoo si es necesario:")
    print("     docker compose restart odoo")
    print()
    sys.exit(1)
