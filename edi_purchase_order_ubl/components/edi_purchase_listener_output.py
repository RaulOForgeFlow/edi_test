from odoo.addons.component.core import Component


class EdiPurchaseListenerOutput(Component):
    _name = "edi.purchase.listener.output"
    _inherit = "base.event.listener"
    _apply_on = "purchase.order"

    def _get_purchase_backend(self, record):
        return record.env.ref("edi_purchase_order_ubl.purchase_backend")

    def _get_backend(self, record):
        return self._get_purchase_backend(record)

    def _get_exchange_record_vals(self, record):
        return {"model": record._name, "res_id": record.id}

    def on_post_purchase(self, record):
        backend = self._get_backend(record)
        exchange_type = "purchase"
        exchange_record = backend.create_record(exchange_type, self._get_exchange_record_vals(record))
        backend.generate_output(exchange_record)
        backend.exchange_send(exchange_record)


