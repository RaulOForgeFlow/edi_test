from odoo import models, fields, api
from ..scripts.gen_json import genJSON

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library to manage books'
    _inherit = "edi.exchange.consumer.mixin"

    name = fields.Char("Title", required=True)
    date_release = fields.Date("Release Date")
    cost_price = fields.Float("Book Cost", digits='Book Price')
    short_name = fields.Char('Short Title', required=True)
    author_ids = fields.Many2many('res.partner', string="Authors")
    description = fields.Html('Description')
    cover = fields.Binary('Book Cover')
    currency = fields.Many2one('res.currency', string="Currency")
    pages = fields.Integer('Number of Pages')

    def generate_book_data(self):
        file = genJSON(self)
        return file
