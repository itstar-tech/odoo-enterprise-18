from odoo import models, fields

class LibraryBookCopy(models.Model):
    _name = 'library.book.copy'
    _description = 'Copia Física de un Libro'
    _rec_name = 'reference_code'

    book_id = fields.Many2one('library.book', string='Libro', required=True, ondelete='cascade')
    reference_code = fields.Char('Código de Referencia', required=True)
    state = fields.Selection([
        ('available', 'Disponible'),
        ('on_loan', 'Prestado'),
        ('reserved', 'Reservado'),
        ('lost', 'Perdido'),
    ], string='Estado', default='available', required=True)
    
   
    _sql_constraints = [
        ('reference_code_unique', 'unique(reference_code)', '¡El código de referencia de la copia ya existe!')
    ]