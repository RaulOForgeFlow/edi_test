from odoo import api, fields, models
from lxml import etree

class AccountMove(models.Model):
    _name = "account.move"
    _inherit = ["account.move", "edi.exchange.consumer.mixin"]

    def send_invoice_button(self):
        self._event("on_post_invoice").notify(self)

    def generate_invoice_data(self):
        etree_root = self.generate_invoice_ubl_xml_etree()
        tree = etree.ElementTree(etree_root)
        with open('/home/ferran/odoo-dev13/edi_test/edi_account_move_ubl/temp_files/temp.xml', "wb") as files:
            tree.write(files)

        invoice_file_bytes = self.generate_ubl_xml_string()
        return invoice_file_bytes

    def receive_invoice_button(self):
        self._event("on_get_invoice").notify(self)





