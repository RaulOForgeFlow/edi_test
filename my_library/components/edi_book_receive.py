# Copyright 2020 Creu Blanca
# @author: Enric Tobella
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component

class EdiWebServiceReceiveFaceL10nEsFacturaeFaceUpdate(Component):
    _name = "edi.webservice.receive.book"
    _usage = "webservice.receive"
    _backend_type = "book"
    _exchange_type = "book_title_update"
    _webservice_protocol = "http"
    _inherit = "edi.component.receive.mixin"

    def receive(self):
        is_new_record = True
        short_name = self.exchange_record.record.short_name
        if short_name != False:
            is_new_record = False

        book_response = self.backend.webservice_backend_id.call(
            "getFTP",
            self.exchange_record.backend_id.webservice_backend_id.url,
            self.exchange_record.backend_id.webservice_backend_id.username,
            self.exchange_record.backend_id.webservice_backend_id.password,
            is_new_record,
            short_name,
        )
        return book_response