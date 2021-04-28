from odoo.addons.component.core import Component
import json
import datetime
import logging

logger = logging.getLogger(__name__)

class EdiSaleProcess(Component):
    _name = "edi.input.process.sale"
    _usage = "input.process"
    _backend_type = "sale"
    _exchange_type = "sale_update"
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

        '''
        #Check whether this short_name already exists or not (similar to a PO ID)
        self.env.cr.execute("""select id from library_book lb where short_name like '{}'""".format(short_name))
        book_ids = [rec[0] for rec in self.env.cr.fetchall()]
        recordset = self.env['library.book'].browse(book_ids)
        if len(recordset) != 0:
            for book_record_short_name in recordset:
                book_record_short_name.write(
                    {'name': book_title,
                     'short_name': short_name,
                     'cost_price': 100,
                     'pages': pages,
                     'description': description,
                     'author_ids': [(6, 0, author_ids)],
                     'currency': currency,
                     # 'cover':cover,
                     }
                )
                if (date_release != False):
                    book_record_short_name.write(
                        {'date_release': datetime.datetime.strptime(date_release, '%Y-%m-%d').date()}
                    )
        
        else:
        '''
        self.exchange_record.record.write(
            {'name': book_title,
             'short_name': short_name,
             'cost_price': cost_price,
             'pages': pages,
             'description': description,
             'author_ids': [(6, 0, author_ids)],
             'currency': currency,
             #'cover':cover,
            }
        )
        if(date_release!=False):
            self.exchange_record.record.write(
                {'date_release': datetime.datetime.strptime(date_release, '%Y-%m-%d').date()}
            )
