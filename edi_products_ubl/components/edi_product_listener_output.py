from odoo.addons.component.core import Component


class EdiProductListenerOutput(Component):
    _name = "edi.product.listener.output"
    _inherit = "base.event.listener"
    _apply_on = "product.pricelist"

    def _get_product_backend(self, record):
        return record.env.ref("edi_products_ubl.product_backend")

    def _get_backend(self, record):
        return self._get_product_backend(record)

    def _get_exchange_record_vals(self, record):
        return {"model": record._name, "res_id": record.id}

    def on_post_product(self, record):
        backend = self._get_backend(record)
        exchange_type = "product"
        exchange_record = backend.create_record(exchange_type, self._get_exchange_record_vals(record))
        backend.generate_output(exchange_record)
        backend.exchange_send(exchange_record)


