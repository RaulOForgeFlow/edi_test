# © 2016-2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# Copyright 2020 Onestein (<https://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
from lxml import etree
from odoo import api, fields, models

logger = logging.getLogger(__name__)


class Product(models.Model):
    _name = "product.catalogue"
    _inherit = ["product.catalogue", "base.ubl"]

    def _ubl_add_item(self, product, parent_node, ns, version="2.1"):
        item = etree.SubElement(parent_node, ns["cac"] + "Item")

        #description = etree.SubElement(item, ns["cbc"] + "Description")
        #description.text = product.description

        name = etree.SubElement(item, ns["cbc"] + "Name")
        name.text = product.name

        seller_item_id = etree.SubElement(item, ns["cac"] + "SellersItemIdentification")
        reference = etree.SubElement(seller_item_id, ns["cbc"] + "ID")
        reference.text = product.partner_ref

        if (product.product_variant_count != 0):
            for attribute_line in product.product_template_attribute_value_ids:
                additional_property = etree.SubElement(item, ns["cac"] + "AdditionalItemProperty")
                property_name = etree.SubElement(additional_property, ns["cbc"] + "Name")
                property_name.text = attribute_line.attribute_id.name
                property_value = etree.SubElement(additional_property, ns["cbc"] + "Value")
                property_value.text = attribute_line.name


    @api.model
    def _ubl_add_provider_party(self, parent_node, ns, version="2.1"):
        provider_party_root = etree.SubElement(parent_node, ns["cac"] + 'ProviderParty')

        party_name = etree.SubElement(provider_party_root, ns["cac"] + "PartyName")
        name = etree.SubElement(party_name, ns["cbc"] + "Name")
        name.text = self.company_id.name


    @api.model
    def _ubl_add_receiver_party(self, parent_node, ns, version="2.1"):
        receiver_party_root = etree.SubElement(parent_node, ns["cac"] + 'ReceiverParty')

        party_name = etree.SubElement(receiver_party_root, ns["cac"] + "PartyName")
        name = etree.SubElement(party_name, ns["cbc"] + "Name")
        # Catalogues can have several partners, so a loop may be needed
        name.text = self.partner_id.name

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
        valueQuantity.text = str(product.list_price)
        valueQualifier = etree.SubElement(item, ns["cbc"] + "ValueQualifier")
        valueQualifier.text = product.cost_currency_id.name


    def _ubl_add_catalogue_line(self, product, catalogue_line_id, parent_node, ns):
        line_root = etree.SubElement(parent_node, ns["cac"] + "CatalogueLine")
        catalogue_id = etree.SubElement(line_root, ns["cbc"] + "ID")
        catalogue_id.text = str(catalogue_line_id)
        self._ubl_add_item(product, line_root, ns)
        self._ubl_add_itemProperty(product, line_root, ns)


    def generate_product_ubl_xml_etree(self, version="2.1"):
        nsmap, ns = self._ubl_get_nsmap_namespace("Catalogue-2", version=version)
        xml_root = etree.Element("Catalogue", nsmap=nsmap)
        self._ubl_add_header(xml_root, ns, version=version)

        self._ubl_add_provider_party(xml_root, ns)
        self._ubl_add_receiver_party(xml_root, ns)

        # Loop on the products in the catalogue
        catalogue_line_id = 0
        for product in self.item_ids:
            catalogue_line_id = catalogue_line_id + 1
            self._ubl_add_catalogue_line(product, catalogue_line_id, xml_root, ns)

        return xml_root

        '''
        self.company_id --------
        self.partner_id --------
        self.name ---------
        self.item_ids
            code
            cost_currency_id
                currency_unit_label (Dollars)
                currency_subunit_label (Cents)
                decimal_places
                display name / name (USD) --------
                rate = 1.2834
                rate_ids
                symbol ($)
            default_code
            description_sale
            display_name ('[17589683] Beeswax')
            image_1024
            list_price ----------
            name ----------
            partner_ref '[17589683] Beeswax' ---------
            product_variant_count
            product_variant_id
            item_number (Gubi Addon)
            free_qty
            incoming_qty
            outgoing_qty
            
            
            
            <cac:SellersItemIdentification>
                <cbc:ID>FURN_0096</cbc:ID>
            </cac:SellersItemIdentification>
            
            <cac:AdditionalItemProperty>
                <cbc:Name>Legs</cbc:Name>
                <cbc:Value>Steel</cbc:Value>
            </cac:AdditionalItemProperty>
            
            AdditionalItemProperty
                
        '''