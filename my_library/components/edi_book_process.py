from odoo.addons.component.core import Component
from odoo import models, fields, api
import json
import datetime
import logging

logger = logging.getLogger(__name__)

class EdiBookProcess(Component):
    _name = "edi.input.process.book"
    _usage = "input.process"
    _backend_type = "book"
    _exchange_type = "book_title_update"
    _inherit = "edi.component.input.mixin"

    def process(self):

        data = json.loads(self.exchange_record._get_file_content())

        book_title = data["name"]
        short_name = data["short_name"]
        cost_price = data["cost_price"]
        pages = data["pages"]
        description = data["description"]
        author_ids = data["author_ids"]
        date_release = data["date_release"]
        currency = data["currency"]
        #cover = data["cover"].encode('utf-8')



        values = {
            'name': book_title,
            'short_name': short_name,
            'cost_price': cost_price,
            'pages': pages,
            'description': description,
            'author_ids': [(6, 0, author_ids)],
            'currency': currency,
        }
        if (date_release != 'False'):
            values['date_release'] = datetime.datetime.strptime(date_release, '%Y-%m-%d').date()

        # Check whether this short_name already exists or not (similar to a PO ID)
        self.env.cr.execute("""select id from library_book lb where short_name like '{}'""".format(short_name))
        book_ids = [rec[0] for rec in self.env.cr.fetchall()]
        recordset = self.env['library.book'].browse(book_ids)
        if len(recordset) != 0:
            for book_record_short_name in recordset:
                book_record_short_name.write(values)
                self.exchange_record.write({
                    'model': 'library.book',
                    'res_id': book_record_short_name.id})
        # If not, create a new book with the information in data
        else:
            lib_book_model = self.env['library.book']
            lib_book_rec = lib_book_model.create(values)
            self.exchange_record.write({
                'model': 'library.book',
                'res_id': lib_book_rec.id})
            print('Hello')