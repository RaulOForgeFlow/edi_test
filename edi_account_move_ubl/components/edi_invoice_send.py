from odoo.addons.component.core import Component


class EdiInvoiceSend(Component):
    _name = "edi.output.send.invoice"
    _usage = "webservice.send"
    _backend_type = "invoice"
    _exchange_type = "invoice"
    _webservice_protocol = "http"
    _inherit = "edi.component.send.mixin"

    def send(self):
        self.backend.webservice_backend_id.call(
            "uploadFTP",
            self.exchange_record.backend_id.webservice_backend_id.url,
            self.exchange_record.backend_id.webservice_backend_id.username,
            self.exchange_record.backend_id.webservice_backend_id.password,
            self.exchange_record.exchange_filename,
            self.exchange_record.backend_id.webservice_backend_id.ftpDirectory,
            self.exchange_record.record.invoice_company.ftp_subdirectory,
        )
