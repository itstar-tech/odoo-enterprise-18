#!/usr/bin/env python3
"""
Script de ejemplo para probar la API REST de la Biblioteca de Odoo
"""

import requests
import json


class LibraryAPIClient:
    """Cliente Python para la API REST de Biblioteca"""
    
    def __init__(self, base_url, api_key):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
    
    def health_check(self):
        """Verifica que la API esté funcionando"""
        url = f"{self.base_url}/api/library/health"
        response = requests.get(url)
        return response.json()
    
    def list_books(self, search=None, limit=10, offset=0):
        """Lista libros con filtros opcionales"""
        url = f"{self.base_url}/api/library/books"
        params = {
            "api_key": self.api_key,
            "limit": limit,
            "offset": offset
        }
        if search:
            params["search"] = search
        
        response = requests.get(url, params=params)
        return response.json()
    
    def get_book(self, book_id):
        """Obtiene detalles de un libro específico"""
        url = f"{self.base_url}/api/library/books/{book_id}"
        params = {"api_key": self.api_key}
        response = requests.get(url, params=params)
        return response.json()
    
    def create_book(self, title, isbn=None, authors=None, sinopsis=None, copies=0):
        """Crea un nuevo libro"""
        url = f"{self.base_url}/api/library/books"
        payload = {
            "jsonrpc": "2.0",
            "params": {
                "api_key": self.api_key,
                "title": title,
                "copies": copies
            }
        }
        
        if isbn:
            payload["params"]["isbn"] = isbn
        if authors:
            payload["params"]["authors"] = authors
        if sinopsis:
            payload["params"]["sinopsis"] = sinopsis
        
        response = requests.post(url, json=payload)
        return response.json()
    
    def update_book(self, book_id, title=None, isbn=None, sinopsis=None):
        """Actualiza un libro existente"""
        url = f"{self.base_url}/web/dataset/call_kw/library.book/write"
        # Nota: Este endpoint usa el método alternativo
        # Puedes implementar el PUT si lo prefieres
        pass
    
    def list_loans(self, state=None, member_id=None, limit=100):
        """Lista préstamos con filtros"""
        url = f"{self.base_url}/api/library/loans"
        params = {
            "api_key": self.api_key,
            "limit": limit
        }
        if state:
            params["state"] = state
        if member_id:
            params["member_id"] = member_id
        
        response = requests.get(url, params=params)
        return response.json()
    
    def create_loan(self, member_id, copy_id, due_days=14, auto_confirm=False):
        """Crea un nuevo préstamo"""
        url = f"{self.base_url}/api/library/loans"
        payload = {
            "jsonrpc": "2.0",
            "params": {
                "api_key": self.api_key,
                "member_id": member_id,
                "copy_id": copy_id,
                "due_days": due_days,
                "auto_confirm": auto_confirm
            }
        }
        
        response = requests.post(url, json=payload)
        return response.json()
    
    def return_loan(self, loan_id):
        """Registra la devolución de un préstamo"""
        url = f"{self.base_url}/api/library/loans/{loan_id}/return"
        payload = {
            "jsonrpc": "2.0",
            "params": {
                "api_key": self.api_key
            }
        }
        
        response = requests.post(url, json=payload)
        return response.json()
    
    def list_members(self, search=None):
        """Lista miembros de la biblioteca"""
        url = f"{self.base_url}/api/library/members"
        params = {"api_key": self.api_key}
        if search:
            params["search"] = search
        
        response = requests.get(url, params=params)
        return response.json()


# ============== EJEMPLOS DE USO ==============

def main():
    """Ejemplos de uso de la API"""
    
    # Configuración
    BASE_URL = "http://localhost:8069"
    API_KEY = "TU_API_KEY_AQUI"  # ⚠️ Reemplaza con tu API key real
    
    # Crear cliente
    client = LibraryAPIClient(BASE_URL, API_KEY)
    
    print("=" * 60)
    print("🧪 PROBANDO API REST DE BIBLIOTECA")
    print("=" * 60)
    
    # 1. Health Check
    print("\n1️⃣  Health Check...")
    try:
        health = client.health_check()
        print(f"✅ API funcionando: {health}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 2. Crear un libro
    print("\n2️⃣  Creando un libro nuevo...")
    try:
        new_book = client.create_book(
            title="Python para Principiantes",
            isbn="9781234567890",
            sinopsis="Un libro excelente para aprender Python desde cero",
            copies=3
        )
        print(f"✅ Libro creado: {json.dumps(new_book, indent=2)}")
        
        if new_book.get('result', {}).get('success'):
            book_id = new_book['result']['data']['id']
        else:
            book_id = None
    except Exception as e:
        print(f"❌ Error: {e}")
        book_id = None
    
    # 3. Listar libros
    print("\n3️⃣  Listando libros...")
    try:
        books = client.list_books(limit=5)
        print(f"✅ Libros encontrados: {books.get('count', 0)}")
        for book in books.get('data', []):
            print(f"   - {book['title']} (ID: {book['id']}, Disponibles: {book['available_copies']})")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 4. Buscar libros
    print("\n4️⃣  Buscando libros con 'Python'...")
    try:
        books = client.list_books(search="Python", limit=5)
        print(f"✅ Libros encontrados: {books.get('count', 0)}")
        for book in books.get('data', []):
            print(f"   - {book['title']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 5. Obtener detalle de un libro
    if book_id:
        print(f"\n5️⃣  Obteniendo detalle del libro ID {book_id}...")
        try:
            book_detail = client.get_book(book_id)
            print(f"✅ Detalle: {json.dumps(book_detail, indent=2)}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # 6. Listar miembros
    print("\n6️⃣  Listando miembros...")
    try:
        members = client.list_members()
        print(f"✅ Miembros encontrados: {members.get('count', 0)}")
        for member in members.get('data', [])[:5]:
            print(f"   - {member['name']} (Préstamos activos: {member['active_loans']})")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 7. Listar préstamos
    print("\n7️⃣  Listando préstamos activos...")
    try:
        loans = client.list_loans(state="active", limit=5)
        print(f"✅ Préstamos activos: {loans.get('count', 0)}")
        for loan in loans.get('data', []):
            print(f"   - {loan['book']['title']} → {loan['member']['name']}")
            print(f"     Vence: {loan['due_date']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 8. Crear un préstamo (comentado para evitar errores si no hay datos)
    print("\n8️⃣  Crear préstamo (ejemplo, no ejecutado)...")
    print("""
    # Para crear un préstamo, necesitas:
    # - member_id: ID de un miembro existente
    # - copy_id: ID de una copia disponible
    
    loan = client.create_loan(
        member_id=5,
        copy_id=2,
        due_days=14,
        auto_confirm=True
    )
    """)
    
    print("\n" + "=" * 60)
    print("✨ PRUEBAS COMPLETADAS")
    print("=" * 60)
    print("\n💡 Tip: Genera tu API Key en Odoo:")
    print("   Ajustes → Usuarios → [Tu Usuario] → Pestaña 'API Access'")
    print("=" * 60)


if __name__ == "__main__":
    main()
