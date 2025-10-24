# -*- coding: utf-8 -*-
import secrets
from odoo import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    # Compatibility field for custom views referencing 'api_key'
    # Note: This is independent from Odoo's standard API Keys (api_key_ids).
    api_key = fields.Char(string='API Key', copy=False)

    def action_regenerate_api_key(self):
        """Regenerate a random API key string for the current user and
        open the standard Odoo modal to display/copy it.
        """
        self.ensure_one()
        new_key = secrets.token_hex(16)  # 32 hex chars
        self.write({'api_key': new_key})
        # Use the built-in tableless wizard to show the key
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
