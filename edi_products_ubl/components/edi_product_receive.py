# Copyright 2020 Creu Blanca
# @author: Enric Tobella
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component

class EdiProductReceive(Component):
    _name = "edi.webservice.receive.product"
    _usage = "webservice.receive"
    _backend_type = "product"
    _exchange_type = "product_update"
    _webservice_protocol = "http"
    _inherit = "edi.component.receive.mixin"

    def receive(self):

        product_response = self.backend.webservice_backend_id.call(
            "getFTP",
            self.exchange_record.backend_id.webservice_backend_id.url,
            self.exchange_record.backend_id.webservice_backend_id.username,
            self.exchange_record.backend_id.webservice_backend_id.password,
        )
        return product_response