from odoo.addons.component.core import Component


class EdiInvoiceReceive(Component):
    _name = "edi.webservice.receive.invoice"
    _usage = "webservice.receive"
    _backend_type = "invoice"
    _exchange_type = "invoice_update"
    _webservice_protocol = "http"
    _inherit = "edi.component.receive.mixin"

    def receive(self):

        book_response = self.backend.webservice_backend_id.call(
            "getFTP",
            self.exchange_record.backend_id.webservice_backend_id.url,
            self.exchange_record.backend_id.webservice_backend_id.username,
            self.exchange_record.backend_id.webservice_backend_id.password,
            self.exchange_record.backend_id.webservice_backend_id.ftpDirectory,
            self.exchange_record.record.invoice_company.ftp_subdirectory,
        )
        return book_response
