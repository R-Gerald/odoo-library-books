# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class LibraryBookCategory(models.Model):
    _name = 'library.book.category'
    _description = 'Library Book Category'

    name = fields.Char(string='Nom', required=True)
    description = fields.Text(string='Description')
    book_ids= fields.One2many('library.book', 'category_id', string='Livres')
    book_count = fields.Integer(string='Nombre de livres', compute='_compute_book_count')
    available_book_count = fields.Integer(string='Livres disponibles',compute='_compute_available_book_count')

    @api.depends('book_ids') 
    def _compute_book_count(self):
        for category in self:
            category.book_count =len(category.book_ids)

    @api.depends('book_ids.is_available')  
    def _compute_available_book_count(self):
        for category in self:
            category.available_book_count = sum(1 for book in category.book_ids if book.is_available)
             
    
    def action_open_books(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': f'Livres de la catégorie {self.name}',
            'res_model': 'library.book',
            'view_mode': 'tree,form',
            'domain': [('category_id', '=', self.id)],
            'context': {'default_category_id': self.id},
        }
        
    


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'

    name = fields.Char(string='Titre', required=True)
    author = fields.Char(string='Auteur')
    published_date = fields.Date(string='Date de publication')
    is_available = fields.Boolean(string='Disponible', default=True)
    category_id = fields.Many2one('library.book.category', string='Catégorie')

    def action_mark_unavailable(self):
        for record in self:
            record.is_available = False

    def action_mark_available(self):
        for record in self:
            record.is_available = True

    def action_test_orm(self):
        new_book = self.env['library.book'].create({
            'name': 'Livre créé par ORM',
            'author': 'Script',
            'is_available': True,
        })

        available_count = self.env['library.book'].search_count([
            ('is_available', '=', True)
        ])

        _logger.info("Nouveau livre créé: %s (ID: %s)", new_book.name, new_book.id)
        _logger.info("Nombre de livres disponibles: %s", available_count)

        return True
    
    def action_mark_all_unavailable(self):
        """Marque tous les livres comme indisponibles."""
        all_books = self.env['library.book'].search([])
        all_books.write({'is_available': False})

    def action_delete_all_unavailable(self):
        """Supprime tous les livres indisponibles."""
        unavailable_books = self.env['library.book'].search([('is_available', '=', False)])
        unavailable_books.unlink()

           
class CrmLead(models.Model):
    _inherit = 'crm.lead'

    project_type = fields.Selection(
        [
            ('small', 'Petit projet'),
            ('medium', 'Projet moyen'),
            ('big', 'Gros projet'),
        ],
        string='Type de projet',
    )

class ResPartner(models.Model):
    _inherit = 'res.partner'

    library_book_ids = fields.Many2many(
        'library.book',
        'partner_library_book_rel',
        'partner_id',
        'book_id',
        string='Livres empruntés'
    )
    @api.constrains('library_book_ids')
    def _check_library_books_available(self):
        for partner in self:
            unavailable_books = partner.library_book_ids.filtered(lambda b: not b.is_available)
            if unavailable_books:
                book_names = ', '.join(unavailable_books.mapped('name'))
                raise ValidationError(f"Le partenaire {partner.name} ne peut pas emprunter les livres suivants car ils sont indisponibles: {book_names}")