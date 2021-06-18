from odoo.addons.component.core import Component


class EdiInvoiceListenerInput(Component):
    _name = "edi.invoice.listener.input"
    _inherit = "base.event.listener"
    _apply_on = ["account.move.import"]

    def _get_exchange_record_vals(self, record):
        return {"model": record._name, "res_id": record.id}

    def on_get_invoice(self, record):

        backend = record.env.ref("edi_account_move_ubl.invoice_backend")
        exchange_type = "invoice_update"

        exchange_record = backend.create_record(
            exchange_type, self._get_exchange_record_vals(record)
        )

        if exchange_record.edi_exchange_state == "new":
            exchange_record.write({"edi_exchange_state": "input_pending"})
        exchange_record.backend_id.with_context(
            _edi_send_break_on_error=True
        ).exchange_receive(exchange_record)
        exchange_record.backend_id.with_context(
            _edi_send_break_on_error=True
        ).exchange_process(exchange_record)
