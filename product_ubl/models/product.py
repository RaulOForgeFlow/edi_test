# © 2016-2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# Copyright 2020 Onestein (<https://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
from lxml import etree
from odoo import api, fields, models

logger = logging.getLogger(__name__)


class Product(models.Model):
    _name = "product.template"
    _inherit = ["product.template", "base.ubl"]



    def _ubl_add_item(self, name, product, parent_node, ns, version = "2.1"):
        item = etree.SubElement(parent_node, ns["cac"] + "Item")
        description = etree.SubElement(item, ns["cbc"] + "Description")
        description.text = name
        name_node = etree.SubElement(item, ns["cbc"] + "Name")
        name_node.text = name.split("\n")[0]

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

    def _ubl_add_catalogue_line(self, parent_node, ns):
        line_root = etree.SubElement(parent_node, ns["cac"] + "CatalogueLine")
        catalogue_id = etree.SubElement(line_root, ns["cbc"] + "ID")
        catalogue_id.text = str(self.id)
        self._ubl_add_item(self.name, self.id, line_root, ns)


    def generate_product_ubl_xml_etree(self, version="2.1"):
        nsmap, ns = self._ubl_get_nsmap_namespace("Catalogue-2", version=version)
        xml_root = etree.Element("Catalogue", nsmap=nsmap)
        self._ubl_add_header(xml_root, ns, version=version)

        self._ubl_add_provider_party(self.env.user.company_id, xml_root, ns)
        self._ubl_add_receiver_party(self.env.user.company_id, xml_root, ns)

        self._ubl_add_catalogue_line(xml_root, ns)

        return xml_root

