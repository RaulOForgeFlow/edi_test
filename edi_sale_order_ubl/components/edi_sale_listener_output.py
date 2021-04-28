from odoo.addons.component.core import Component


class EdiSaleListenerOutput(Component):
    _name = "edi.sale.listener.output"
    _inherit = "base.event.listener"
    _apply_on = "sale.order"

    def _get_sale_backend(self, record):
        return record.env.ref("edi_sale_order_ubl.sale_backend")

    def _get_backend(self, record):
        return self._get_sale_backend(record)

    def _get_exchange_record_vals(self, record):
        return {"model": record._name, "res_id": record.id}

    def on_post_sale(self, record):
        backend = self._get_backend(record)
        exchange_type = "sale"
        exchange_record = backend.create_record(exchange_type, self._get_exchange_record_vals(record))
        backend.generate_output(exchange_record)
        backend.exchange_send(exchange_record)


