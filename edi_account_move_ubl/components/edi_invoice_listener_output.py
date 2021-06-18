from odoo.addons.component.core import Component


class EdiInvoiceListenerOutput(Component):
    _name = "edi.invoice.listener.output"
    _inherit = "base.event.listener"
    _apply_on = "account.move"

    def _get_exchange_record_vals(self, record):
        return {"model": record._name, "res_id": record.id}

    def on_post_invoice(self, record):
        backend = record.env.ref("edi_account_move_ubl.invoice_backend")
        exchange_type = "invoice"
        exchange_record = backend.create_record(
            exchange_type, self._get_exchange_record_vals(record)
        )
        backend.generate_output(exchange_record)
        backend.exchange_send(exchange_record)
