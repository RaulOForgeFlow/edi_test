from odoo.addons.component.core import Component


class EdiInvoiceListenerOutput(Component):
    _name = "edi.invoice.listener.output"
    _inherit = "base.event.listener"
    _apply_on = "account.move"

    def _get_invoice_backend(self, record):
        return record.env.ref("edi_account_move_ubl.invoice_backend")

    def _get_backend(self, record):
        return self._get_invoice_backend(record)

    def _get_exchange_record_vals(self, record):
        return {"model": record._name, "res_id": record.id}

    def on_post_invoice(self, record):
        backend = self._get_backend(record)
        exchange_type = "invoice"
        exchange_record = backend.create_record(exchange_type, self._get_exchange_record_vals(record))
        backend.generate_output(exchange_record)
        backend.exchange_send(exchange_record)


