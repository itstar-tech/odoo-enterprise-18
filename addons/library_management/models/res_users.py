# -*- coding: utf-8 -*-
from odoo import models, fields, api
import secrets


class ResUsers(models.Model):
    _inherit = 'res.users'

    api_key = fields.Char(
        string='API Key',
        help='Clave de API para autenticación en endpoints REST',
        copy=False,
        groups='base.group_system'
    )

    def generate_api_key(self):
        """Genera una nueva API key aleatoria"""
        for user in self:
            user.api_key = secrets.token_urlsafe(32)

    def action_regenerate_api_key(self):
        """Acción de botón para regenerar API key"""
        self.generate_api_key()
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'message': 'Nueva API Key generada exitosamente',
                'type': 'success',
                'sticky': False,
            }
        }
