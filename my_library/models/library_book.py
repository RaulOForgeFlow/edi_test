from odoo import models, fields, api
from ..scripts.gen_json import genJSON
from ..scripts.num_files_ftp import count_files
from odoo.exceptions import UserError

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'
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

    def get_book_info(self):
        files_FTP = count_files()
        num_files = len(files_FTP)

        if num_files == 0:
            raise UserError("There are no files to receive in the FTP server. Please upload first at least one")
        else:
            self._event("on_get_book_title").notify(self)

    def update_book_info(self):
        self._event("on_get_book_title").notify(self)

    def generate_book_data(self):
        file = genJSON(self)
        return file

