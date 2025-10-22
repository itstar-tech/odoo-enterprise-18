# -*- coding: utf-8 -*-
{
    'name': "Gestión de Biblioteca",
    'summary': """
        Gestiona préstamos, libros y miembros de una biblioteca.""",
    'description': """
        Módulo completo para administrar una biblioteca.
    """,
    'author': "Darvin Luna",
    'website': "https://darvinluna.com",
    'category': 'Services/Library',
    'version': '1.0',
    'license': 'LGPL-3',
    
    # 'depends' es crucial. Necesitamos 'base' siempre, 
    # y 'mail' para las notificaciones y seguidores (ej. "libro devuelto").
    'depends': ['base', 'mail'],

    # 'data' es la lista de archivos XML que cargará (Vistas y Seguridad)
    'data': [
        # 1. Seguridad (SIEMPRE PRIMERO)
        'security/ir.model.access.csv',
        
        # 2. Vistas (El orden aquí no es crítico, pero es bueno tener menús al final)
        'views/library_book_views.xml',
        'views/library_loan_views.xml',
        'views/res_partner_views.xml',
        'views/res_users_views.xml',
        
        # 3. Menús (SIEMPRE DESPUÉS DE LAS VISTAS/ACCIONES que usan)
        'views/library_menus.xml',
    ],
    'application': True, # Esto lo hace una "App" completa en Odoo.
}