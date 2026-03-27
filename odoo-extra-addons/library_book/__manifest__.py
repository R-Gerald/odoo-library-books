# -*- coding: utf-8 -*-
{
    'name': 'Library Book',
    'version': '1.0',
    'summary': 'Simple module to manage books',
    'description': """
Library Book
============

Module bibliothèque pour apprendre le développement Odoo.
""",
    'author': 'Gerald',
    'category': 'Tools',
    'depends': ['base', 'crm'],
    'data': [
        'security/ir.model.access.csv',
        'views/library_book_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'library_book/static/src/js/availability_widget.js',
            'library_book/static/src/xml/availability_widget.xml',
            'library_book/static/src/js/library_dashboard.js',
            'library_book/static/src/xml/library_dashboard.xml',
        ],
    },
    'installable': True,
    'application': True,
}