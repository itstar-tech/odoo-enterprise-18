# -*- coding: utf-8 -*-
from odoo import models, fields


class ApiKeyShow(models.TransientModel):
    _name = 'library.api.key.show'
    _description = 'Mostrar API Key Generada'

    key = fields.Char(
        string='API Key',
        readonly=True,
        help='Esta es tu API Key. Guárdala en un lugar seguro, no se volverá a mostrar.'
    )
    message = fields.Text(
        string='Mensaje',
        readonly=True,
        default='¡API Key generada exitosamente! Cópiala ahora, no se volverá a mostrar por seguridad.'
    )
