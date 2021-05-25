# Copyright 2020 Creu Blanca
# @author: Enric Tobella
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component

class EdiProductListenerInput(Component):
    _name = "edi.product.listener.input"
    _inherit = "base.event.listener"
    _apply_on = ["product.catalogue"]

    def _get_product_backend(self, record):
        return record.env.ref("edi_product_ubl.product_backend")

    def _get_backend(self, record):
        return self._get_product_backend(record)

    def _get_exchange_record_vals(self, record):
        return {"model": record._name, "res_id": record.id}

    def on_get_product(self, record):

        backend = self._get_backend(record)
        exchange_type = "product_update"

        exchange_record = backend.create_record(exchange_type, self._get_exchange_record_vals(record))

        if exchange_record.edi_exchange_state == "new":
            exchange_record.write(
                {"edi_exchange_state": "input_pending"})
        exchange_record.backend_id.with_context(_edi_send_break_on_error=True).exchange_receive(exchange_record)
        exchange_record.backend_id.with_context(_edi_send_break_on_error=True).exchange_process(exchange_record)

