# © 2016-2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# Copyright 2020 Onestein (<https://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
from lxml import etree
from odoo import api, fields, models

logger = logging.getLogger(__name__)


class Product(models.Model):
    _name = "product.pricelist"
    _inherit = ["product.pricelist", "base.ubl"]

    def _ubl_add_item(self, product, parent_node, ns, version="2.1"):
        item = etree.SubElement(parent_node, ns["cac"] + "Item")
        description = etree.SubElement(item, ns["cbc"] + "Description")
        description.text = product.product_tmpl_id.name
        #price = etree.SubElement(item, ns["cbc"] + "Price")
        #price.text = str(product.product_tmpl_id.list_price)
        # The following fields can be accessed via the product.product_tmpl_id
        # cost_currency_id, default_code(E-COM11), id, image_1920(bytes type), name, list_price ...
    @api.model
    def _ubl_add_provider_party(self, company, parent_node, ns, version="2.1"):
        provider_party_root = etree.SubElement(parent_node, ns["cac"] + 'ProviderParty')

        party_name = etree.SubElement(provider_party_root, ns["cac"] + "PartyName")
        name = etree.SubElement(party_name, ns["cbc"] + "Name")
        name.text = company.name


    @api.model
    def _ubl_add_receiver_party(self, company, parent_node, ns, version="2.1"):
        receiver_party_root = etree.SubElement(parent_node, ns["cac"] + 'ReceiverParty')

        party_name = etree.SubElement(receiver_party_root, ns["cac"] + "PartyName")
        name = etree.SubElement(party_name, ns["cbc"] + "Name")
        name.text = company.name

    def _ubl_add_header(self, parent_node, ns, version="2.1"):
        now_utc = fields.Datetime.to_string(fields.Datetime.now())
        date = now_utc[:10]
        ubl_version = etree.SubElement(parent_node, ns["cbc"] + "UBLVersionID")
        ubl_version.text = version
        doc_id = etree.SubElement(parent_node, ns["cbc"] + "ID")
        doc_id.text = self.name
        issue_date = etree.SubElement(parent_node, ns["cbc"] + "IssueDate")
        issue_date.text = date

    def _ubl_add_itemProperty(self, product, parent_node, ns):
        item = etree.SubElement(parent_node, ns["cac"] + "ItemProperty")
        valueQuantity = etree.SubElement(item, ns["cbc"] + "ValueQuantity")
        valueQuantity.text = str(product.product_tmpl_id.list_price)
        valueQualifier = etree.SubElement(item, ns["cbc"] + "ValueQualifier")
        valueQualifier.text = product.product_tmpl_id.cost_currency_id.name


    def _ubl_add_catalogue_line(self, product, parent_node, ns):
        line_root = etree.SubElement(parent_node, ns["cac"] + "CatalogueLine")
        catalogue_id = etree.SubElement(line_root, ns["cbc"] + "ID")
        catalogue_id.text = str(product.product_tmpl_id.id)
        self._ubl_add_item(product, line_root, ns)
        self._ubl_add_itemProperty(product, line_root, ns)


    def generate_product_ubl_xml_etree(self, version="2.1"):
        nsmap, ns = self._ubl_get_nsmap_namespace("Catalogue-2", version=version)
        xml_root = etree.Element("Catalogue", nsmap=nsmap)
        self._ubl_add_header(xml_root, ns, version=version)

        self._ubl_add_provider_party(self.env.user.company_id, xml_root, ns)
        self._ubl_add_receiver_party(self.env.user.company_id, xml_root, ns)

        # Loop on the products in the pricelist
        pricelist_products = self.env['product.pricelist.item'].search([('pricelist_id','=',self.id)])
        for product in pricelist_products:
            self._ubl_add_catalogue_line(product, xml_root, ns)

        return xml_root

