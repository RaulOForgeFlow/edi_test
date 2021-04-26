from odoo import api, fields, models
from lxml import etree

class AccountMove(models.Model):
    _name = "sale.order"
    _inherit = ["sale.order", "edi.exchange.consumer.mixin"]

    def send_sale_button(self):
        self._event("on_post_sale").notify(self)

    def generate_sale_data(self):
        '''
        etree_root = self.generate_order_response_simple_ubl_xml_etree()
        tree = etree.ElementTree(etree_root)
        tree.write('/home/ferran/odoo-dev13/edi_test/edi_sale_order_ubl/temp_files/temp.xml')
        '''

        sale_order_file_bytes = self.generate_ubl_xml_string('quotation')

        file = open('/home/ferran/odoo-dev13/edi_test/edi_sale_order_ubl/temp_files/temp.xml', 'wb')
        file.write(sale_order_file_bytes)
        file.close()


        return sale_order_file_bytes

    def receive_sale_button(self):
        self._event("on_get_sale").notify(self)





