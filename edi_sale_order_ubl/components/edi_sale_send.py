# Copyright 2020 Creu Blanca
# @author: Enric Tobella
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component

class EdiBookSend(Component):
    _name = "edi.output.send.sale"
    _usage = "webservice.send"
    _backend_type = "sale"
    _exchange_type = "sale"
    _webservice_protocol = "http"
    _inherit = "edi.component.send.mixin"

    def send(self):
        self.backend.webservice_backend_id.call(
            "uploadFTP",
            self.exchange_record.backend_id.webservice_backend_id.url,
            self.exchange_record.backend_id.webservice_backend_id.username,
            self.exchange_record.backend_id.webservice_backend_id.password,
            self.exchange_record.exchange_filename,
        )
