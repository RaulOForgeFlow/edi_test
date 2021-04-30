from odoo import api, fields, models

class PurchaseOrder(models.Model):
    _name = "purchase.order"
    _inherit = ["purchase.order", "edi.exchange.consumer.mixin"]

    def send_purchase_button(self):
        self._event("on_post_purchase").notify(self)

    def generate_purchase_data(self):

        if self.state == 'draft' or self.state == 'sent':
            purchase_order_file_bytes = self.generate_ubl_xml_string('rfq')
        elif self.state == 'purchase':
            purchase_order_file_bytes = self.generate_ubl_xml_string('order')

        file = open('/home/ferran/odoo-dev13/edi_test/edi_purchase_order_ubl/temp_files/temp.xml', 'wb')
        file.write(purchase_order_file_bytes)
        file.close()

        return purchase_order_file_bytes

    def receive_purchase_button(self):
        self._event("on_get_purchase").notify(self)





