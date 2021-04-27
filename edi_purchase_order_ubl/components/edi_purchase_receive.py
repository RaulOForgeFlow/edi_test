# Copyright 2020 Creu Blanca
# @author: Enric Tobella
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component

class EdiPurchaseReceive(Component):
    _name = "edi.webservice.receive.purchase"
    _usage = "webservice.receive"
    _backend_type = "purchase"
    _exchange_type = "purchase_update"
    _webservice_protocol = "http"
    _inherit = "edi.component.receive.mixin"

    def receive(self):

        book_response = self.backend.webservice_backend_id.call(
            "getFTP",
            self.exchange_record.backend_id.webservice_backend_id.url,
            self.exchange_record.backend_id.webservice_backend_id.username,
            self.exchange_record.backend_id.webservice_backend_id.password,
        )
        return book_response