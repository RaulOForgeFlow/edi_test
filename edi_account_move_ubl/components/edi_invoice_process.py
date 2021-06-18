from lxml import etree as ET

from odoo.addons.component.core import Component


class EdiInvoiceProcess(Component):
    _name = "edi.input.process.invoice"
    _usage = "input.process"
    _backend_type = "invoice"
    _exchange_type = "invoice_update"
    _inherit = "edi.component.input.mixin"

    def process(self):

        file_content = self.exchange_record._get_file_content()
        xml_root = ET.fromstring(file_content)
        self.exchange_record.record.create_invoice_from_attachment(xml_root)
