from odoo import models, fields, api

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Libro de Biblioteca (Plantilla)'
    _inherit = ['mail.thread', 'mail.activity.mixin'] # Para notificaciones

    name = fields.Char('Título', required=True)
    author_ids = fields.Many2many('res.partner', string='Autores')
    isbn = fields.Char('ISBN', size=13)
    sinopsis = fields.Text('Sinopsis')
    

    copy_ids = fields.One2many('library.book.copy', 'book_id', string='Copias')
    

    availability = fields.Selection([
        ('available', 'Disponible'),
        ('on_loan', 'Prestado'),
        ('not_available', 'No Disponible (0 copias)')
    ], string='Disponibilidad', compute='_compute_availability')

    @api.depends('copy_ids.state')
    def _compute_availability(self):
        for book in self:
            available_copies = book.copy_ids.filtered(lambda c: c.state == 'available')
            if available_copies:
                book.availability = 'available'
            elif book.copy_ids.filtered(lambda c: c.state == 'on_loan'):
                book.availability = 'on_loan'
            else:
                book.availability = 'not_available'