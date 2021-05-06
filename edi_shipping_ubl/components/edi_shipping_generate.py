from odoo.addons.component.core import Component

class EdiShippingGenerate(Component):
    _name = "edi.output.generate.shipping"
    _inherit = "edi.component.output.mixin"
    _usage = "output.generate"
    _backend_type = "shipping"

    def generate(self):
        return self.exchange_record.record.generate_shipping_data()

