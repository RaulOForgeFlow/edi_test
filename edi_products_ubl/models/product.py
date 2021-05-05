# © 2016-2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# Copyright 2020 Onestein (<https://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
from lxml import etree
from odoo import api, fields, models

logger = logging.getLogger(__name__)


class Product(models.Model):
    _name = "product.pricelist"
    _inherit = ["product.pricelist", "edi.exchange.consumer.mixin"]

    def send_product_button(self):
        self._event("on_post_product").notify(self)

    def generate_product_data(self):
        xml_root = self.generate_product_ubl_xml_etree()
        xml_bytes = etree.tostring(xml_root, pretty_print=True, encoding="UTF-8", xml_declaration=True)
        xml_str = xml_bytes.decode(encoding="UTF-8")

        file = open('/home/ferran/odoo-dev13/edi_test/edi_products_ubl/temp_files/temp.xml', 'w')
        file.write(xml_str)
        file.close()

        return xml_bytes



