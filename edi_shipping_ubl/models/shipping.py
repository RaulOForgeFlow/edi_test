# © 2016-2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# Copyright 2020 Onestein (<https://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
from lxml import etree
from odoo import api, fields, models

logger = logging.getLogger(__name__)


class Shipping(models.Model):
    _name = "stock.picking"
    _inherit = ["stock.picking", "edi.exchange.consumer.mixin"]

    def send_shipping_button(self):
        self._event("on_post_shipping").notify(self)

    def generate_shipping_data(self):
        xml_root = self.generate_shipping_ubl_xml_etree()
        xml_bytes = etree.tostring(xml_root, pretty_print=True, encoding="UTF-8", xml_declaration=True)
        xml_str = xml_bytes.decode(encoding="UTF-8")

        #file = open('/home/raul/local-odoo/odoo-dev13/edi_test/edi_shipping_ubl/temp_files/temp.xml', 'w')
        file = open('/home/ferran/odoo-dev13/edi_test/edi_shipping_ubl/temp_files/temp.xml', 'w')
        file.write(xml_str)
        file.close()

        return xml_bytes



