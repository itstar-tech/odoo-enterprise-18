# -*- coding: utf-8 -*-
import secrets
from odoo import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    api_key = fields.Char(
        string='API Key (Legacy)',
        copy=False,
        help='Campo legacy para compatibilidad. Use el sistema de API Keys nativo de Odoo (Preferencias > API Keys)'
    )

    def action_regenerate_api_key(self):
        """
        Regenera una clave API legacy y la muestra en un modal.
        NOTA: Para usar auth='bearer' en controladores, se recomienda usar
        el sistema nativo de API Keys de Odoo: Preferencias de Usuario > API Keys
        """
        self.ensure_one()
        new_key = secrets.token_hex(16)
        self.write({'api_key': new_key})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'res.users.apikeys.show',
            'name': 'API Key Ready',
            'views': [(False, 'form')],
            'target': 'new',
            'context': {
                'default_key': new_key,
            },
        }

    @property
    def SELF_READABLE_FIELDS(self):
        # Ensure the field is readable on the user preferences form
        return super().SELF_READABLE_FIELDS + ['api_key']

    @property
    def SELF_WRITEABLE_FIELDS(self):
        # Allow users to write their own api_key via this method/context
        return super().SELF_WRITEABLE_FIELDS + ['api_key']
