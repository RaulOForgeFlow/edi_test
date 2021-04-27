from odoo.addons.component.core import Component

class EdiPurchaseGenerate(Component):
    _name = "edi.output.generate.purchase"
    _inherit = "edi.component.output.mixin"
    _usage = "output.generate"
    _backend_type = "purchase"

    def generate(self):
        return self.exchange_record.record.generate_purchase_data()

