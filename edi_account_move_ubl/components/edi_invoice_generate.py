from odoo.addons.component.core import Component

class EdiBookGenerate(Component):
    _name = "edi.output.generate.invoice"
    _inherit = "edi.component.output.mixin"
    _description = "Generates the book in edi format"
    _usage = "output.generate"
    _backend_type = "invoice"

    def generate(self):
        return self.exchange_record.record.generate_invoice_data()

