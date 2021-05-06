# Copyright 2020 Creu Blanca
# @author: Enric Tobella
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component

class EdiShippingListenerInput(Component):
    _name = "edi.product.listener.input"
    _inherit = "base.event.listener"
    _apply_on = ["stock.picking"]

    def _get_shipping_backend(self, record):
        return record.env.ref("edi_shipping_ubl.shipping_backend")

    def _get_backend(self, record):
        return self._get_shipping_backend(record)

    def _get_exchange_record_vals(self, record):
        return {"model": record._name, "res_id": record.id}

    def on_get_shipping(self, record):

        backend = self._get_backend(record)
        exchange_type = "shipping_update"

        exchange_record = backend.create_record(exchange_type, self._get_exchange_record_vals(record))

        if exchange_record.edi_exchange_state == "new":
            exchange_record.write(
                {"edi_exchange_state": "input_pending"})
        exchange_record.backend_id.with_context(_edi_send_break_on_error=True).exchange_receive(exchange_record)
        exchange_record.backend_id.with_context(_edi_send_break_on_error=True).exchange_process(exchange_record)

