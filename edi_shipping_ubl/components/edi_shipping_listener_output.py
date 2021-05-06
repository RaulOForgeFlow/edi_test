from odoo.addons.component.core import Component


class EdiShippingListenerOutput(Component):
    _name = "edi.shipping.listener.output"
    _inherit = "base.event.listener"
    _apply_on = "stock.picking"

    def _get_shipping_backend(self, record):
        return record.env.ref("edi_shipping_ubl.shipping_backend")

    def _get_backend(self, record):
        return self._get_shipping_backend(record)

    def _get_exchange_record_vals(self, record):
        return {"model": record._name, "res_id": record.id}

    def on_post_shipping(self, record):
        backend = self._get_backend(record)
        exchange_type = "shipping"
        exchange_record = backend.create_record(exchange_type, self._get_exchange_record_vals(record))
        backend.generate_output(exchange_record)
        backend.exchange_send(exchange_record)


