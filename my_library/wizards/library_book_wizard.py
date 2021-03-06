from odoo import models, fields, api
from ..scripts.num_files_ftp import count_files
from odoo.exceptions import UserError

class LibraryBookWizard(models.TransientModel):
    _name = "library.book.wizard"
    _description = "Wizard for Library Books"
    _inherit = ["library.book", "edi.exchange.consumer.mixin"]

    name = fields.Char("Title", required=False)
    short_name = fields.Char('Short Title', required=False)

    def get_book_info(self):
        files_FTP = count_files('my_library')
        num_files = len(files_FTP)

        if num_files == 0:
            raise UserError("There are no files to receive in the FTP server. Please upload first at least one")
        else:
            # Update and receive all the books at once
            for rep in range(num_files):
                self._event("on_get_book_title").notify(self)

    def post_book_title(self):
        lib_books = self.env['library.book'].search([])
        for record in lib_books:
            self._event("on_post_book_title").notify(record)