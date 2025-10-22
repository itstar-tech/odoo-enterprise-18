# -*- coding: utf-8 -*-
import json
import logging
from odoo import http
from odoo.http import request, Response
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)


class LibraryAPIController(http.Controller):
    """
    API REST para la gestión de biblioteca
    Permite integración con aplicaciones externas
    """

    def _authenticate(self, api_key):
        """
        Autenticación mediante API Key
        La API Key debe estar configurada en el usuario
        """
        if not api_key:
            _logger.warning("No se proporcionó API key")
            return None
        
        try:
            _logger.info(f"Intentando autenticar con API key: {api_key[:10]}...")
            
            # Verificar que el modelo tiene el campo api_key
            user_model = request.env['res.users'].sudo()
            if 'api_key' not in user_model._fields:
                _logger.error("El campo 'api_key' no existe en el modelo res.users")
                return None
            
            # Usar una nueva transacción para evitar problemas
            with request.env.cr.savepoint():
                # Buscar usuario con esta API key
                user = user_model.search([
                    ('api_key', '=', api_key),
                    ('active', '=', True)
                ], limit=1)
                
                if user:
                    _logger.info(f"Usuario autenticado: {user.login}")
                else:
                    _logger.warning(f"No se encontró usuario con esta API key")
                
                return user if user else None
        except Exception as e:
            _logger.error(f"Error en autenticación: {str(e)}", exc_info=True)
            return None

    def _json_response(self, data, status=200):
        """Helper para crear respuestas JSON consistentes"""
        return Response(
            json.dumps(data, default=str, ensure_ascii=False),
            status=status,
            mimetype='application/json',
            headers={'Content-Type': 'application/json; charset=utf-8'}
        )

    def _error_response(self, message, status=400):
        """Helper para respuestas de error"""
        return self._json_response({
            'success': False,
            'error': message
        }, status=status)

    # ==================== LIBROS ====================

    @http.route('/api/library/books', type='http', auth='public', methods=['GET'], csrf=False)
    def get_books(self, **kwargs):
        """
        Obtener lista de libros
        
        Parámetros:
        - api_key: Clave de API (obligatorio)
        - limit: Número máximo de resultados (default: 100)
        - offset: Desplazamiento para paginación (default: 0)
        - search: Búsqueda por título o autor
        
        Ejemplo: /api/library/books?api_key=YOUR_KEY&limit=10&search=Python
        """
        try:
            api_key = kwargs.get('api_key')
            user = self._authenticate(api_key)
            
            if not user:
                return self._error_response('API key inválida o faltante', 401)

            # Parámetros de búsqueda
            limit = int(kwargs.get('limit', 100))
            offset = int(kwargs.get('offset', 0))
            search = kwargs.get('search', '')

            # Construir dominio de búsqueda
            domain = []
            if search:
                domain = ['|', ('name', 'ilike', search), ('author_ids.name', 'ilike', search)]

            # Buscar libros
            books = request.env['library.book'].sudo().search(domain, limit=limit, offset=offset)
            
            # Formatear respuesta
            books_data = []
            for book in books:
                books_data.append({
                    'id': book.id,
                    'title': book.name,
                    'isbn': book.isbn or '',
                    'authors': [{'id': a.id, 'name': a.name} for a in book.author_ids],
                    'sinopsis': book.sinopsis or '',
                    'availability': book.availability,
                    'total_copies': len(book.copy_ids),
                    'available_copies': len(book.copy_ids.filtered(lambda c: c.state == 'available'))
                })

            return self._json_response({
                'success': True,
                'count': len(books_data),
                'total': request.env['library.book'].sudo().search_count(domain),
                'data': books_data
            })

        except Exception as e:
            _logger.error(f"Error en get_books: {str(e)}")
            return self._error_response(str(e), 500)

    @http.route('/api/library/books/<int:book_id>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_book_detail(self, book_id, **kwargs):
        """
        Obtener detalle de un libro específico
        
        Parámetros:
        - api_key: Clave de API (obligatorio)
        
        Ejemplo: /api/library/books/1?api_key=YOUR_KEY
        """
        try:
            api_key = kwargs.get('api_key')
            user = self._authenticate(api_key)
            
            if not user:
                return self._error_response('API key inválida o faltante', 401)

            book = request.env['library.book'].sudo().browse(book_id)
            
            if not book.exists():
                return self._error_response('Libro no encontrado', 404)

            # Información de copias
            copies_data = []
            for copy in book.copy_ids:
                copies_data.append({
                    'id': copy.id,
                    'reference_code': copy.reference_code,
                    'state': copy.state
                })

            return self._json_response({
                'success': True,
                'data': {
                    'id': book.id,
                    'title': book.name,
                    'isbn': book.isbn or '',
                    'authors': [{'id': a.id, 'name': a.name} for a in book.author_ids],
                    'sinopsis': book.sinopsis or '',
                    'availability': book.availability,
                    'copies': copies_data
                }
            })

        except Exception as e:
            _logger.error(f"Error en get_book_detail: {str(e)}")
            return self._error_response(str(e), 500)

    @http.route('/api/library/books', type='http', auth='public', methods=['POST'], csrf=False)
    def create_book(self, **kwargs):
        """
        Crear un nuevo libro
        
        Body JSON:
        {
            "name": "Título del libro",
            "isbn": "1234567890123",
            "author": "Nombre del autor",
            "pages": 350,
            "publication_year": 2024
        }
        
        API Key: Se pasa como query parameter ?api_key=YOUR_KEY
        
        Ejemplo con curl:
        curl -X POST "http://localhost:8069/api/library/books?api_key=YOUR_KEY" \
          -H "Content-Type: application/json" \
          -d '{"name":"Python Programming","isbn":"1234567890123","author":"Guido","pages":500}'
        """
        try:
            api_key = kwargs.get('api_key')
            user = self._authenticate(api_key)
            
            if not user:
                return self._error_response('API key inválida o faltante', 401)

            # Leer JSON del body
            try:
                data = json.loads(request.httprequest.data.decode('utf-8'))
            except:
                return self._error_response('JSON inválido', 400)

            # Validar datos requeridos
            if not data.get('name'):
                return self._error_response('El nombre del libro es obligatorio', 400)

            # Crear libro
            book_vals = {
                'name': data.get('name'),
                'isbn': data.get('isbn', ''),
            }

            # Agregar autor como partner si se proporciona
            if data.get('author'):
                # Buscar o crear el autor como partner
                author = request.env['res.partner'].sudo().search([
                    ('name', '=', data.get('author'))
                ], limit=1)
                if not author:
                    author = request.env['res.partner'].sudo().create({
                        'name': data.get('author'),
                        'is_library_member': True
                    })
                book_vals['author_ids'] = [(4, author.id)]

            book = request.env['library.book'].sudo().create(book_vals)

            # Crear una copia por defecto
            request.env['library.book.copy'].sudo().create({
                'book_id': book.id,
                'reference_code': f"{book.isbn or 'BOOK'}-{book.id}-1",
                'state': 'available'
            })

            return self._json_response({
                'success': True,
                'message': 'Libro creado exitosamente',
                'data': {
                    'id': book.id,
                    'name': book.name,
                    'isbn': book.isbn,
                    'authors': [a.name for a in book.author_ids]
                }
            })

        except Exception as e:
            _logger.error(f"Error en create_book: {str(e)}", exc_info=True)
            return self._error_response(str(e), 500)

    @http.route('/api/library/books/<int:book_id>', type='http', auth='public', methods=['PUT'], csrf=False)
    def update_book(self, book_id, **kwargs):
        """
        Actualizar un libro existente
        
        Body JSON:
        {
            "name": "Nuevo título",
            "isbn": "9876543210987",
            "pages": 600
        }
        
        API Key: Se pasa como query parameter ?api_key=YOUR_KEY
        """
        try:
            api_key = kwargs.get('api_key')
            user = self._authenticate(api_key)
            
            if not user:
                return self._error_response('API key inválida o faltante', 401)

            # Leer JSON del body
            try:
                data = json.loads(request.httprequest.data.decode('utf-8'))
            except:
                return self._error_response('JSON inválido', 400)

            book = request.env['library.book'].sudo().browse(book_id)
            
            if not book.exists():
                return self._error_response('Libro no encontrado', 404)

            # Actualizar campos
            update_vals = {}
            if data.get('name'):
                update_vals['name'] = data.get('name')
            if 'isbn' in data:
                update_vals['isbn'] = data.get('isbn')

            if update_vals:
                book.write(update_vals)

            return self._json_response({
                'success': True,
                'message': 'Libro actualizado exitosamente',
                'data': {
                    'id': book.id,
                    'name': book.name,
                    'isbn': book.isbn
                }
            })

        except Exception as e:
            _logger.error(f"Error en update_book: {str(e)}", exc_info=True)
            return self._error_response(str(e), 500)

    # ==================== PRÉSTAMOS ====================

    @http.route('/api/library/loans', type='http', auth='public', methods=['GET'], csrf=False)
    def get_loans(self, **kwargs):
        """
        Obtener lista de préstamos
        
        Parámetros:
        - api_key: Clave de API (obligatorio)
        - state: Filtrar por estado (draft, active, returned, overdue)
        - member_id: Filtrar por ID de miembro
        - limit: Número máximo de resultados (default: 100)
        
        Ejemplo: /api/library/loans?api_key=YOUR_KEY&state=active
        """
        try:
            api_key = kwargs.get('api_key')
            user = self._authenticate(api_key)
            
            if not user:
                return self._error_response('API key inválida o faltante', 401)

            # Parámetros de búsqueda
            limit = int(kwargs.get('limit', 100))
            domain = []

            if kwargs.get('state'):
                domain.append(('state', '=', kwargs.get('state')))
            if kwargs.get('member_id'):
                domain.append(('member_id', '=', int(kwargs.get('member_id'))))

            # Buscar préstamos
            loans = request.env['library.loan'].sudo().search(domain, limit=limit, order='loan_date desc')
            
            loans_data = []
            for loan in loans:
                loans_data.append({
                    'id': loan.id,
                    'member': {
                        'id': loan.member_id.id,
                        'name': loan.member_id.name,
                        'email': loan.member_id.email or ''
                    },
                    'book': {
                        'id': loan.book_id.id,
                        'title': loan.book_id.name
                    },
                    'copy_id': loan.copy_id.id,
                    'loan_date': loan.loan_date.isoformat() if loan.loan_date else None,
                    'due_date': loan.due_date.isoformat() if loan.due_date else None,
                    'return_date': loan.return_date.isoformat() if loan.return_date else None,
                    'state': loan.state
                })

            return self._json_response({
                'success': True,
                'count': len(loans_data),
                'data': loans_data
            })

        except Exception as e:
            _logger.error(f"Error en get_loans: {str(e)}")
            return self._error_response(str(e), 500)

    @http.route('/api/library/loans', type='http', auth='public', methods=['POST'], csrf=False)
    def create_loan(self, **kwargs):
        """
        Crear un nuevo préstamo
        
        Body JSON:
        {
            "member_id": 1,
            "copy_id": 2,
            "due_days": 14  // Días hasta vencimiento (opcional, default: 14)
        }
        
        API Key: Se pasa como query parameter ?api_key=YOUR_KEY
        """
        try:
            api_key = kwargs.get('api_key')
            user = self._authenticate(api_key)
            
            if not user:
                return self._error_response('API key inválida o faltante', 401)

            # Leer JSON del body
            try:
                data = json.loads(request.httprequest.data.decode('utf-8'))
            except:
                return self._error_response('JSON inválido', 400)

            # Validar datos
            if not data.get('member_id') or not data.get('copy_id'):
                return self._error_response('member_id y copy_id son obligatorios', 400)

            # Verificar que la copia esté disponible
            copy = request.env['library.book.copy'].sudo().browse(data.get('copy_id'))
            if not copy.exists():
                return self._error_response('Copia no encontrada', 404)

            if copy.state != 'available':
                return self._error_response(f'La copia no está disponible (estado: {copy.state})', 400)

            # Crear préstamo
            due_days = data.get('due_days', 14)
            loan_vals = {
                'member_id': data.get('member_id'),
                'copy_id': data.get('copy_id'),
                'loan_date': datetime.now().date(),
                'due_date': (datetime.now() + timedelta(days=due_days)).date(),
                'state': 'draft'
            }

            loan = request.env['library.loan'].sudo().create(loan_vals)

            # Si se especifica, confirmar el préstamo automáticamente
            if data.get('auto_confirm', False):
                loan.action_loan()

            return self._json_response({
                'success': True,
                'message': 'Préstamo creado exitosamente',
                'data': {
                    'id': loan.id,
                    'member': loan.member_id.name,
                    'book': loan.book_id.name,
                    'due_date': loan.due_date.isoformat(),
                    'state': loan.state
                }
            })

        except Exception as e:
            _logger.error(f"Error en create_loan: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    @http.route('/api/library/loans/<int:loan_id>/return', type='http', auth='public', methods=['POST'], csrf=False)
    def return_loan(self, loan_id, **kwargs):
        """
        Registrar devolución de un préstamo
        
        API Key: Se pasa como query parameter ?api_key=YOUR_KEY
        """
        try:
            api_key = kwargs.get('api_key')
            user = self._authenticate(api_key)
            
            if not user:
                return self._error_response('API key inválida o faltante', 401)

            loan = request.env['library.loan'].sudo().browse(loan_id)
            
            if not loan.exists():
                return self._error_response('Préstamo no encontrado', 404)

            if loan.state != 'active':
                return self._error_response(f'El préstamo no está activo (estado: {loan.state})', 400)

            loan.action_return()

            return self._json_response({
                'success': True,
                'message': 'Préstamo devuelto exitosamente',
                'data': {
                    'id': loan.id,
                    'return_date': loan.return_date.isoformat(),
                    'state': loan.state
                }
            })

        except Exception as e:
            _logger.error(f"Error en return_loan: {str(e)}", exc_info=True)
            return self._error_response(str(e), 500)
            _logger.error(f"Error en return_loan: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    # ==================== MIEMBROS ====================

    @http.route('/api/library/members', type='http', auth='public', methods=['GET'], csrf=False)
    def get_members(self, **kwargs):
        """
        Obtener lista de miembros de la biblioteca
        
        Parámetros:
        - api_key: Clave de API (obligatorio)
        - search: Búsqueda por nombre o email
        
        Ejemplo: /api/library/members?api_key=YOUR_KEY&search=juan
        """
        try:
            api_key = kwargs.get('api_key')
            user = self._authenticate(api_key)
            
            if not user:
                return self._error_response('API key inválida o faltante', 401)

            domain = [('is_library_member', '=', True)]
            search = kwargs.get('search', '')
            
            if search:
                domain += ['|', ('name', 'ilike', search), ('email', 'ilike', search)]

            members = request.env['res.partner'].sudo().search(domain, limit=100)
            
            members_data = []
            for member in members:
                members_data.append({
                    'id': member.id,
                    'name': member.name,
                    'email': member.email or '',
                    'phone': member.phone or '',
                    'active_loans': len(member.loan_ids.filtered(lambda l: l.state == 'active'))
                })

            return self._json_response({
                'success': True,
                'count': len(members_data),
                'data': members_data
            })

        except Exception as e:
            _logger.error(f"Error en get_members: {str(e)}")
            return self._error_response(str(e), 500)

    # ==================== UTILIDADES ====================

    @http.route('/api/library/health', type='http', auth='public', methods=['GET'], csrf=False)
    def health_check(self, **kwargs):
        """
        Endpoint de salud para verificar que la API está funcionando
        
        Ejemplo: /api/library/health
        """
        return self._json_response({
            'success': True,
            'message': 'Library API is running',
            'version': '1.0',
            'timestamp': datetime.now().isoformat()
        })
