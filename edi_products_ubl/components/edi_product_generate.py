from odoo.addons.component.core import Component

class EdiProductGenerate(Component):
    _name = "edi.output.generate.product"
    _inherit = "edi.component.output.mixin"
    _usage = "output.generate"
    _backend_type = "product"

    def generate(self):
        return self.exchange_record.record.generate_product_data()

