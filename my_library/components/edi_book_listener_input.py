# Copyright 2020 Creu Blanca
# @author: Enric Tobella
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component
from odoo.exceptions import UserError
from odoo import _

class EdiBookListenerInput(Component):
    _name = "edi.book.listener.input"
    _inherit = "base.event.listener"
    _apply_on = ["library.book","library.book.wizard"]

    def _get_book_backend(self, record):
        return record.env.ref("my_library.book_backend")

    def _get_backend(self, record):
        return self._get_book_backend(record)

    def _get_exchange_record_vals(self, record):
        return {"model": record._name, "res_id": record.id}

    def on_get_book_title(self, record):

        backend = self._get_backend(record)
        exchange_type = "book_title_update"

        exchange_record = backend.create_record(exchange_type, self._get_exchange_record_vals(record))
        # Create an exchange record with no vals in it (record/model associated library.book and with no record id of library.book)
        # Receive the file and insert it into the exchange record in the Exchange File field
        # When processing it and determinig if the short_name is already on the database, a new record is created and associated to the created exchange record
        # book = self.env["library.book"]
        # book_record = book.create(vals)

        if exchange_record.edi_exchange_state == "new":
            exchange_record.write(
                {"edi_exchange_state": "input_pending"})
        exchange_record.backend_id.with_context(_edi_send_break_on_error=True).exchange_receive(exchange_record)
        exchange_record.backend_id.with_context(_edi_send_break_on_error=True).exchange_process(exchange_record)

