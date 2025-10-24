# -*- coding: utf-8 -*-
from odoo import models, fields


class ShowApiKeyWizard(models.TransientModel):
    _name = 'library.show.api.key'
    _description = 'Mostrar Clave API'

    key = fields.Char(string='Clave API', readonly=True)

