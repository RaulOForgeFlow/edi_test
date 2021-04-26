# Copyright 2020 Creu Blanca
# @author: Enric Tobella
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component

class EdiBookGenerate(Component):
    _name = "edi.output.generate.book"
    _inherit = "edi.component.output.mixin"
    _usage = "output.generate"
    _backend_type = "book"

    def generate(self):
        # returns a dictionary in [0] and [1] the new file_name
        data_and_filename = self.exchange_record.record.generate_book_data()

        self.exchange_record.exchange_filename = data_and_filename[1]
        return data_and_filename[0]


