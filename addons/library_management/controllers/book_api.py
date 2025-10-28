# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request, Response


class LibraryBookAPI(http.Controller):
    """
    API JSON-RPC para gestionar libros de biblioteca.
    Usa autenticación estándar de Odoo (usuario/contraseña/base de datos).
    """

    @http.route('/api/library/authenticate', type='json', auth='none', methods=['POST'], csrf=False)
    def authenticate(self, db, login, password):
        """
        Autentica un usuario y devuelve su UID.
        
        Uso:
        {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "db": "library_management",
                "login": "admin",
                "password": "admin"
            },
            "id": 1
        }
        
        Retorna: {"uid": <user_id>}
        """
        try:
            uid = request.session.authenticate(db, login, password)
            if not uid:
                return {'error': 'Credenciales inválidas'}
            return {'uid': uid}
        except Exception as e:
            return {'error': str(e)}

    @http.route('/api/library/books/search', type='json', auth='user', methods=['POST'], csrf=False)
    def search_books(self, search=None, limit=100):
        """
        Busca libros en la biblioteca.
        
        Uso:
        {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "search": "Quijote",
                "limit": 10
            },
            "id": 1
        }
        
        Retorna: [{"id": 1, "name": "...", "isbn": "...", ...}]
        """
        try:
            domain = []
            if search:
                domain.append(('name', 'ilike', search))

            books = request.env['library.book'].search(domain, limit=limit)
            book_data = books.read(['id', 'name', 'isbn', 'availability'])

            return {'books': book_data, 'count': len(book_data)}
        except Exception as e:
            return {'error': str(e)}

    @http.route('/api/library/books/create', type='json', auth='user', methods=['POST'], csrf=False)
    def create_book(self, name, isbn=None, **kwargs):
        """
        Crea un nuevo libro.
        
        Uso:
        {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "name": "El Principito",
                "isbn": "978-0156012195"
            },
            "id": 1
        }
        
        Retorna: {"id": <book_id>, "name": "..."}
        """
        try:
            if not name or not name.strip():
                return {'error': "El campo 'name' es obligatorio."}

            new_book = request.env['library.book'].create({
                'name': name.strip(),
                'isbn': isbn,
            })

            return {
                'id': new_book.id,
                'name': new_book.name,
                'isbn': new_book.isbn,
                'availability': new_book.availability
            }
        except Exception as e:
            return {'error': str(e)}

    @http.route('/api/library/books/read', type='json', auth='user', methods=['POST'], csrf=False)
    def read_book(self, book_id, fields=None):
        """
        Lee los datos de un libro específico.
        
        Uso:
        {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "book_id": 1,
                "fields": ["id", "name", "isbn", "availability"]
            },
            "id": 1
        }
        
        Retorna: {"id": 1, "name": "...", ...}
        """
        try:
            if not book_id:
                return {'error': 'Se requiere book_id'}

            book = request.env['library.book'].browse(book_id)
            if not book.exists():
                return {'error': f'Libro con ID {book_id} no encontrado'}

            if not fields:
                fields = ['id', 'name', 'isbn', 'availability']

            book_data = book.read(fields)[0]
            return book_data
        except Exception as e:
            return {'error': str(e)}

    @http.route('/api/library/books/update', type='json', auth='user', methods=['POST'], csrf=False)
    def update_book(self, book_id, values):
        """
        Actualiza un libro existente.
        
        Uso:
        {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "book_id": 1,
                "values": {
                    "name": "Nuevo nombre",
                    "isbn": "9876543210"
                }
            },
            "id": 1
        }
        
        Retorna: {"success": true, "id": <book_id>}
        """
        try:
            if not book_id:
                return {'error': 'Se requiere book_id'}

            if not values or not isinstance(values, dict):
                return {'error': 'Se requiere un diccionario de valores'}

            book = request.env['library.book'].browse(book_id)
            if not book.exists():
                return {'error': f'Libro con ID {book_id} no encontrado'}

            book.write(values)

            return {
                'success': True,
                'id': book.id,
                'updated_fields': list(values.keys())
            }
        except Exception as e:
            return {'error': str(e)}

    @http.route('/api/library/books/delete', type='json', auth='user', methods=['POST'], csrf=False)
    def delete_book(self, book_id):
        """
        Elimina un libro.
        
        Uso:
        {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "book_id": 1
            },
            "id": 1
        }
        
        Retorna: {"success": true, "deleted_id": <book_id>}
        """
        try:
            if not book_id:
                return {'error': 'Se requiere book_id'}

            book = request.env['library.book'].browse(book_id)
            if not book.exists():
                return {'error': f'Libro con ID {book_id} no encontrado'}

            deleted_id = book.id
            book.unlink()

            return {
                'success': True,
                'deleted_id': deleted_id
            }
        except Exception as e:
            return {'error': str(e)}

    @http.route('/api/library/ping', type='json', auth='none', methods=['POST'], csrf=False)
    def ping(self):
        """
        Health check endpoint para confirmar que la API está funcionando.
        
        Uso:
        {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {},
            "id": 1
        }
        
        Retorna: {"status": "ok", "message": "API funcionando correctamente"}
        """
        return {
            'status': 'ok',
            'message': 'API funcionando correctamente',
            'version': '1.0'
        }
