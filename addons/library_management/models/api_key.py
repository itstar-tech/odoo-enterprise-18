# -*- coding: utf-8 -*-
import secrets
import hashlib
from datetime import datetime, timedelta
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ApiKey(models.Model):
    _name = 'library.api.key'
    _description = 'API Key para acceso externo'
    _order = 'create_date desc'

    name = fields.Char(
        string='Nombre/Descripción',
        required=True,
        help='Descripción de para qué se usa esta API Key'
    )
    key_prefix = fields.Char(
        string='Prefijo de Clave',
        readonly=True,
        help='Primeros caracteres de la clave para identificación'
    )
    key_hash = fields.Char(
        string='Hash de la Clave',
        required=True,
        readonly=True,
        help='Hash SHA-256 de la clave (nunca se almacena la clave real)'
    )
    user_id = fields.Many2one(
        'res.users',
        string='Usuario Asociado',
        required=True,
        ondelete='cascade',
        help='Usuario cuyos permisos se usarán con esta API Key'
    )
    active = fields.Boolean(
        string='Activa',
        default=True,
        help='Si está inactiva, la clave no puede usarse'
    )
    expires_at = fields.Datetime(
        string='Expira el',
        help='Fecha de expiración. Dejar vacío para que nunca expire'
    )
    last_used_at = fields.Datetime(
        string='Último Uso',
        readonly=True,
        help='Última vez que se usó esta API Key'
    )
    usage_count = fields.Integer(
        string='Número de Usos',
        default=0,
        readonly=True,
        help='Contador de veces que se ha usado esta clave'
    )
    max_usage = fields.Integer(
        string='Uso Máximo',
        help='Número máximo de veces que puede usarse. 0 = ilimitado'
    )
    allowed_ips = fields.Text(
        string='IPs Permitidas',
        help='Lista de IPs permitidas (una por línea). Vacío = todas las IPs'
    )
    rate_limit = fields.Integer(
        string='Límite de Peticiones/Hora',
        default=100,
        help='Número máximo de peticiones por hora. 0 = sin límite'
    )
    request_count_hour = fields.Integer(
        string='Peticiones (Última Hora)',
        default=0,
        readonly=True,
        help='Contador de peticiones en la última hora'
    )
    last_rate_reset = fields.Datetime(
        string='Último Reseteo de Rate Limit',
        readonly=True,
        default=fields.Datetime.now
    )
    scope = fields.Selection([
        ('read', 'Solo Lectura'),
        ('write', 'Lectura y Escritura'),
        ('full', 'Acceso Completo')
    ], string='Alcance', default='read', required=True)

    _sql_constraints = [
        ('key_hash_unique', 'unique(key_hash)', 'Esta API Key ya existe')
    ]

    @api.model
    def generate_key(self, name, user_id, expires_in_days=None, scope='read', max_usage=0, rate_limit=100,
                     allowed_ips=None):
        """
        Genera una nueva API Key
        
        Args:
            name: Descripción de la clave
            user_id: ID del usuario asociado
            expires_in_days: Días hasta expiración (None = nunca expira)
            scope: Alcance de permisos (read, write, full)
            max_usage: Número máximo de usos (0 = ilimitado)
            rate_limit: Peticiones por hora permitidas
            allowed_ips: Lista de IPs permitidas (string con IPs separadas por líneas)
            
        Returns:
            tuple: (api_key_record, plain_text_key)
        """
        plain_key = f"lbk_{secrets.token_urlsafe(32)}"
        key_hash = hashlib.sha256(plain_key.encode()).hexdigest()
        key_prefix = plain_key[:12]

        expires_at = None
        if expires_in_days:
            expires_at = datetime.now() + timedelta(days=expires_in_days)

        api_key = super(ApiKey, self).create({
            'name': name,
            'key_prefix': key_prefix,
            'key_hash': key_hash,
            'user_id': user_id,
            'expires_at': expires_at,
            'scope': scope,
            'max_usage': max_usage,
            'rate_limit': rate_limit,
            'allowed_ips': allowed_ips,
        })

        return api_key, plain_key

    def validate_key(self, plain_key, client_ip=None):
        """
        Valida una API Key
        
        Args:
            plain_key: Clave en texto plano a validar
            client_ip: IP del cliente (opcional)
            
        Returns:
            dict: {'valid': bool, 'error': str, 'user_id': int, 'scope': str}
        """
        self.ensure_one()

        if not self.active:
            return {'valid': False, 'error': 'API Key inactiva', 'code': 'inactive'}

        key_hash = hashlib.sha256(plain_key.encode()).hexdigest()
        if self.key_hash != key_hash:
            return {'valid': False, 'error': 'API Key inválida', 'code': 'invalid'}

        if self.expires_at and datetime.now() > self.expires_at:
            return {'valid': False, 'error': 'API Key expirada', 'code': 'expired'}

        if self.max_usage > 0 and self.usage_count >= self.max_usage:
            return {'valid': False, 'error': 'Límite de uso alcanzado', 'code': 'usage_limit'}

        if client_ip and self.allowed_ips:
            allowed_ips = [ip.strip() for ip in self.allowed_ips.split('\n') if ip.strip()]
            if client_ip not in allowed_ips:
                return {'valid': False, 'error': f'IP {client_ip} no permitida', 'code': 'ip_blocked'}

        if self.rate_limit > 0:
            hours_since_reset = (datetime.now() - self.last_rate_reset).total_seconds() / 3600
            if hours_since_reset >= 1:
                self.write({
                    'request_count_hour': 1,
                    'last_rate_reset': datetime.now()
                })
            else:
                if self.request_count_hour >= self.rate_limit:
                    return {'valid': False, 'error': 'Límite de peticiones excedido', 'code': 'rate_limit'}
                self.write({'request_count_hour': self.request_count_hour + 1})

        self.write({
            'last_used_at': datetime.now(),
            'usage_count': self.usage_count + 1
        })

        return {
            'valid': True,
            'user_id': self.user_id.id,
            'scope': self.scope,
            'username': self.user_id.name
        }

    @api.model
    def find_and_validate(self, plain_key, client_ip=None):
        """
        Busca y valida una API Key
        
        Args:
            plain_key: Clave en texto plano
            client_ip: IP del cliente
            
        Returns:
            dict: Resultado de validación
        """
        if not plain_key or not plain_key.startswith('lbk_'):
            return {'valid': False, 'error': 'Formato de API Key inválido', 'code': 'invalid_format'}

        key_hash = hashlib.sha256(plain_key.encode()).hexdigest()
        api_key = self.search([('key_hash', '=', key_hash)], limit=1)

        if not api_key:
            return {'valid': False, 'error': 'API Key no encontrada', 'code': 'not_found'}

        return api_key.validate_key(plain_key, client_ip)

    def action_rotate_key(self):
        """
        Rota (regenera) la API Key manteniendo la misma configuración
        
        Returns:
            dict: Acción para mostrar la nueva clave
        """
        self.ensure_one()

        plain_key = f"lbk_{secrets.token_urlsafe(32)}"
        key_hash = hashlib.sha256(plain_key.encode()).hexdigest()
        key_prefix = plain_key[:12]

        self.write({
            'key_prefix': key_prefix,
            'key_hash': key_hash,
            'usage_count': 0,
            'last_used_at': False,
            'request_count_hour': 0,
            'last_rate_reset': datetime.now()
        })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'library.api.key.show',
            'name': 'API Key Rotada',
            'views': [(False, 'form')],
            'target': 'new',
            'context': {
                'default_key': plain_key,
                'default_message': f'API Key rotada exitosamente para: {self.name}'
            },
        }

    def action_revoke(self):
        """
        Revoca (desactiva) la API Key
        """
        self.ensure_one()
        self.write({'active': False})
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'API Key Revocada',
                'message': f'La API Key "{self.name}" ha sido revocada y ya no puede usarse.',
                'type': 'success',
                'sticky': False,
            }
        }
