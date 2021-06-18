import os

from lxml import etree

from odoo import models


class AccountMove(models.Model):
    _name = "account.move"
    _inherit = ["account.move", "edi.exchange.consumer.mixin"]

    def send_invoice_button(self):
        self._event("on_post_invoice").notify(self)

    def generate_invoice_data(self, file_name):
        etree_root = self.generate_invoice_ubl_xml_etree()
        tree = etree.ElementTree(etree_root)

        filepath = (
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            + "/temp_files/"
            + file_name
        )
        with open(filepath, "wb") as files:
            tree.write(files)

        invoice_file_bytes = self.generate_ubl_xml_string()
        return invoice_file_bytes
