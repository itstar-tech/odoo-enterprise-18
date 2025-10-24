# -*- coding: utf-8 -*-
{
    'name': "Gestión de Biblioteca",
    'summary': """
        Gestiona préstamos, libros y miembros de una biblioteca.""",
    'description': """
        Módulo completo para administrar una biblioteca.
    """,
    'author': "Darvin Luna",
    'website': "https://github.com/DarvinLuna",
    'category': 'Services/Library',
    'version': '1.0',
    'license': 'LGPL-3',
    

    'depends': ['base', 'mail', 'web'],

    'data': [
        # 1. Seguridad (SIEMPRE PRIMERO)
        'security/ir.model.access.csv',

        'views/library_book_views.xml',
        'views/library_loan_views.xml',
        'views/res_partner_views.xml',
        'views/show_api_key_views.xml',

        'views/library_menus.xml',
    ],
    'application': True, # Esto lo hace una "App" completa en Odoo.
}