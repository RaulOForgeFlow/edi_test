from odoo.addons.component.core import Component

class EdiSaleGenerate(Component):
    _name = "edi.output.generate.sale"
    _inherit = "edi.component.output.mixin"
    _usage = "output.generate"
    _backend_type = "sale"

    def generate(self):
        return self.exchange_record.record.generate_sale_data()

