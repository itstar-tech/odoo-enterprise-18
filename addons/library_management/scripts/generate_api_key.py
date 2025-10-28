#!/usr/bin/env python3
"""
Script para generar una API Key desde Odoo shell

Uso:
    odoo-bin shell -d TU_DB --shell-file=scripts/generate_api_key.py
"""

print("=" * 70)
print(" Generador de API Key - Módulo Biblioteca")
print("=" * 70)
print()

try:
    admin_user = env['res.users'].search([('login', '=', 'admin')], limit=1)
    if not admin_user:
        print("❌ Error: No se encontró el usuario 'admin'")
        exit(1)

    api_key_model = env['library.api.key']

    api_key_record, plain_key = api_key_model.generate_key(
        name='API Key de Prueba - Generada Automáticamente',
        user_id=admin_user.id,
        scope='write',
        rate_limit=100,
        expires_days=30
    )

    env.cr.commit()

    print("✅ API Key generada exitosamente!")
    print()
    print("📋 Detalles:")
    print(f"   ID: {api_key_record.id}")
    print(f"   Nombre: {api_key_record.name}")
    print(f"   Usuario: {api_key_record.user_id.name}")
    print(f"   Scope: {api_key_record.scope}")
    print(f"   Rate Limit: {api_key_record.rate_limit} req/hora")
    print(f"   Expira: {api_key_record.expires_at}")
    print()
    print("🔑 TU API KEY:")
    print(f"   {plain_key}")
    print()
    print("⚠️  IMPORTANTE: Copia esta clave ahora. No se volverá a mostrar.")
    print()
    print("📖 Ejemplo de uso:")
    print(f'   curl -H "X-API-Key: {plain_key}" \\')
    print('        http://localhost:8069/api/library/books')
    print()
    print("🧪 Ejecutar pruebas:")
    print(f"   cd addons/library_management/examples")
    print(f"   python3 test_complete_api.py {plain_key}")
    print()

except Exception as e:
    print(f"❌ Error al generar API Key: {e}")
    import traceback

    traceback.print_exc()
    env.cr.rollback()
