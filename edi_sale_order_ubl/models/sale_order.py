from odoo import api, fields, models
from lxml import etree

class AccountMove(models.Model):
    _name = "sale.order"
    _inherit = ["sale.order", "edi.exchange.consumer.mixin"]

    def send_sale_button(self):
        self._event("on_post_sale").notify(self)

    def generate_sale_data(self):

        sale_order_file_bytes = self.generate_ubl_xml_string('order')
        sale_order_file_str = sale_order_file_bytes.decode(encoding="UTF-8")

        file = open('/home/ferran/odoo-dev13/edi_test/edi_sale_order_ubl/temp_files/temp.xml', 'wb')
        file.write(sale_order_file_bytes)
        file.close()

        return sale_order_file_bytes





