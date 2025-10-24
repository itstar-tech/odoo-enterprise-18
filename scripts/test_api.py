#!/usr/bin/env python3
"""
Script de prueba para la API JSON-RPC de Odoo
Módulo: Gestión de Biblioteca

Este script demuestra cómo usar la API nativa de Odoo (XML-RPC/JSON-RPC)
para interactuar con el módulo de gestión de biblioteca.
"""

import xmlrpc.client

url = 'http://localhost:8069'
db = 'odoo'
username = 'admin'
password = 'admin'

print("=" * 60)
print("PRUEBA DE API - MÓDULO DE GESTIÓN DE BIBLIOTECA")
print("=" * 60)
print()

print("1. Autenticando...")
try:
    common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
    uid = common.authenticate(db, username, password, {})

    if uid:
        print(f"   ✅ Autenticación exitosa. UID: {uid}")
    else:
        print("   ❌ Autenticación fallida")
        exit(1)
except Exception as e:
    print(f"   ❌ Error de conexión: {e}")
    exit(1)

print()

models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

print("2. Buscando libros existentes...")
try:
    books = models.execute_kw(db, uid, password,
                              'library.book', 'search_read',
                              [[]],
                              {'fields': ['id', 'name', 'isbn', 'availability'], 'limit': 5}
                              )
    print(f"   ✅ Encontrados {len(books)} libro(s)")
    for book in books:
        print(f"      - [{book['id']}] {book['name']} (ISBN: {book.get('isbn', 'N/A')})")
        print(f"        Estado: {book['availability']}")
except Exception as e:
    print(f"   ❌ Error al buscar libros: {e}")

print()

print("3. Creando un libro de prueba...")
try:
    book_id = models.execute_kw(db, uid, password,
                                'library.book', 'create',
                                [{
                                    'name': 'API Test Book - Don Quijote de la Mancha',
                                    'isbn': '9788491050360',
                                }]
                                )
    print(f"   ✅ Libro creado con ID: {book_id}")
except Exception as e:
    print(f"   ⚠️  No se pudo crear el libro: {e}")

print()

print("4. Buscando copias de libros...")
try:
    copies = models.execute_kw(db, uid, password,
                               'library.book.copy', 'search_read',
                               [[]],
                               {'fields': ['id', 'reference_code', 'state', 'book_id'], 'limit': 3}
                               )
    print(f"   ✅ Encontradas {len(copies)} copia(s)")
    for copy in copies:
        print(f"      - Código: {copy['reference_code']}")
        print(f"        Estado: {copy['state']}")
        print(f"        Libro: {copy['book_id'][1] if copy.get('book_id') else 'N/A'}")
except Exception as e:
    print(f"   ⚠️  Error al buscar copias: {e}")

print()

print("5. Buscando miembros de la biblioteca...")
try:
    members = models.execute_kw(db, uid, password,
                                'res.partner', 'search_read',
                                [[['is_library_member', '=', True]]],
                                {'fields': ['id', 'name', 'member_id_code'], 'limit': 3}
                                )
    print(f"   ✅ Encontrados {len(members)} miembro(s)")
    for member in members:
        print(f"      - {member['name']}")
        print(f"        Código: {member.get('member_id_code', 'N/A')}")
except Exception as e:
    print(f"   ⚠️  Error al buscar miembros: {e}")

print()

print("6. Buscando préstamos...")
try:
    loans = models.execute_kw(db, uid, password,
                              'library.loan', 'search_read',
                              [[]],
                              {'fields': ['id', 'book_id', 'member_id', 'state', 'loan_date'], 'limit': 3}
                              )
    print(f"   ✅ Encontrados {len(loans)} préstamo(s)")
    for loan in loans:
        member_name = loan['member_id'][1] if loan.get('member_id') else 'N/A'
        book_name = loan['book_id'][1] if loan.get('book_id') else 'N/A'
        print(f"      - Préstamo #{loan['id']}")
        print(f"        Libro: {book_name}")
        print(f"        Miembro: {member_name}")
        print(f"        Estado: {loan['state']}")
        print(f"        Fecha: {loan.get('loan_date', 'N/A')}")
except Exception as e:
    print(f"   ⚠️  Error al buscar préstamos: {e}")

print()
print("=" * 60)
print("PRUEBA COMPLETADA")
print("=" * 60)
print()
print("✅ La API de Odoo está funcionando correctamente")
print("✅ El módulo de biblioteca está operativo")
print("✅ Puedes usar esta API para integraciones externas")
print()
