from odoo import models, fields, api
from ..scripts.gen_json import genJSON
from ..scripts.num_files_ftp import count_files
from odoo.exceptions import UserError

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library to manage books'
    _inherit = "edi.exchange.consumer.mixin"

    name = fields.Char("Title", requiered=True)
    date_release = fields.Date("Release Date")
    cost_price = fields.Float("Book Cost", digits='Book Price')
    short_name = fields.Char('Short Title', requiered=True)
    author_ids = fields.Many2many('res.partner', string="Authors")
    description = fields.Html('Description')
    cover = fields.Binary('Book Cover')
    currency = fields.Many2one('res.currency', string="Currency")
    pages = fields.Integer('Number of Pages')


    def post_book_title(self):
        self._event("on_post_book_title").notify(self)

    def generate_book_data(self):
        file = genJSON(self)
        return file
