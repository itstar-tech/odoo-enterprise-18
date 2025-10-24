# -*- coding: utf-8 -*-
import json
from odoo import http
from odoo.http import request, Response


def _authenticate_api_key():
    """Authenticate the request using an API key.
    Accepts the key from:
    - HTTP header: X-API-Key
    - Query param: api_key
    - JSON body: {"api_key": "..."}

    Returns: (user_record | None, error_response | None)
    """
    api_key = request.httprequest.headers.get('X-API-Key')
    if not api_key:
        api_key = request.params.get('api_key')
    if not api_key:
        try:
            body = request.httprequest.json
            if isinstance(body, dict):
                api_key = body.get('api_key')
        except Exception:
            api_key = None

    if not api_key:
        return None, Response(
            json.dumps({'error': 'Unauthorized: missing API key'}),
            content_type='application/json',
            status=401,
        )

    user = request.env['res.users'].sudo().search([('api_key', '=', api_key), ('active', '=', True)], limit=1)
    if not user:
        return None, Response(
            json.dumps({'error': 'Unauthorized: invalid API key'}),
            content_type='application/json',
            status=401,
        )
    return user, None


class BookAPIController(http.Controller):
    """
    Controlador de API REST para el modelo library.book
    Protegido por API Key simple (res.users.api_key).
    """

    @http.route('/api/ping', type='http', auth='public', methods=['GET'], website=False, csrf=False)
    def ping(self, **kwargs):
        """
        Health check endpoint to confirm controllers are loaded
        """
        return Response('ok', content_type='text/plain', status=200)

    @http.route('/api/library/books', type='http', auth='public', methods=['GET'], website=False, csrf=False)
    def search_books(self, search=None, **kwargs):
        """
        Busca libros en la biblioteca.
        Requiere API key en header X-API-Key o en ?api_key=.
        Ejemplo: /api/library/books?search=Quijote
        """
        user, error = _authenticate_api_key()
        if error:
            return error

        try:
            domain = []
            if search:
                domain.append(('name', 'ilike', search))
            books = request.env['library.book'].sudo().search(domain)
            book_data = books.read(['id', 'name', 'isbn', 'availability'])
            return Response(
                json.dumps(book_data),
                content_type='application/json',
                status=200
            )
        except Exception as e:
            return Response(
                json.dumps({'error': str(e)}),
                content_type='application/json',
                status=500
            )

    @http.route('/api/library/books', type='http', auth='public', methods=['POST'], website=False, csrf=False)
    def create_book(self, **kwargs):
        """
        Crea un nuevo libro.
        Requiere API key. Cuerpo JSON con los datos del libro.
        Ejemplo: {"name": "El Principito", "isbn": "1234567890"}
        """
        user, error = _authenticate_api_key()
        if error:
            return error

        try:
            data = request.httprequest.json or {}

            # Validación simple
            name = (data.get('name') or '').strip()
            if not name:
                raise ValueError("El campo 'name' es obligatorio.")

            new_book = request.env['library.book'].sudo().create({
                'name': name,
                'isbn': data.get('isbn'),
            })

            response_data = {
                'id': new_book.id,
                'name': new_book.name
            }
            return Response(
                json.dumps(response_data),
                content_type='application/json',
                status=201
            )
        except ValueError as ve:
            return Response(
                json.dumps({'error': str(ve)}),
                content_type='application/json',
                status=400
            )
        except Exception as e:
            return Response(
                json.dumps({'error': str(e)}),
                content_type='application/json',
                status=500
            )