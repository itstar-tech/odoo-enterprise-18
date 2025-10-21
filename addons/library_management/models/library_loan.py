from odoo import models, fields, api
from odoo.exceptions import ValidationError

class LibraryLoan(models.Model):
    _name = 'library.loan'
    _description = 'Préstamo de Biblioteca'

    member_id = fields.Many2one(
        'res.partner', 
        string='Miembro', 
        required=True,
        domain="[('is_library_member', '=', True)]" 
    )
    copy_id = fields.Many2one(
        'library.book.copy', 
        string='Copia del Libro', 
        required=True
    )

    book_id = fields.Many2one(
        'library.book', 
        string='Libro',
        related='copy_id.book_id',
        readonly=True
    )
    loan_date = fields.Date('Fecha de Préstamo', default=fields.Date.today)
    due_date = fields.Date('Fecha de Vencimiento', required=True)
    return_date = fields.Date('Fecha de Devolución')
    
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('active', 'Activo'), 
        ('returned', 'Devuelto'),
        ('overdue', 'Atrasado'), 
    ], string='Estado', default='draft')

  

    def action_loan(self):
        """ Lógica para confirmar el préstamo """
        for loan in self:
            if loan.copy_id.state != 'available':
                raise ValidationError(f"¡La copia '{loan.copy_id.reference_code}' no está disponible!")
            
            # 1. Cambiar estado de la copia
            loan.copy_id.write({'state': 'on_loan'})
            # 2. Cambiar estado del préstamo
            loan.write({'state': 'active'})

    def action_return(self):
        """ Lógica para registrar la devolución """
        for loan in self:
            # 1. Cambiar estado de la copia
            loan.copy_id.write({'state': 'available'})
            # 2. Cambiar estado del préstamo
            loan.write({
                'state': 'returned',
                'return_date': fields.Date.today()
            })