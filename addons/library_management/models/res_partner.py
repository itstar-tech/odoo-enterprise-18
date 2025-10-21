from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_library_member = fields.Boolean('Es Miembro de Biblioteca')
    member_id_code = fields.Char('Cód. Miembro')
    
    loan_ids = fields.One2many('library.loan', 'member_id', string='Préstamos')