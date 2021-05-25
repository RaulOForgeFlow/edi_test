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

    # The retailer, who sends this message
    @api.model
    def _ubl_add_retailer_customer_party(self, parent_node, ns, version="2.1"):
        '''
        CustomerAssignedAccountID
            ID
        Party
            PartyIdentification
                ID
            PartyName
                Name
            PostalAddress
                ID
                AddressLine
                    Line
        '''
        provider_party_root = etree.SubElement(parent_node, ns["cac"] + 'ProviderParty')

        party_name = etree.SubElement(provider_party_root, ns["cac"] + "PartyName")
        name = etree.SubElement(party_name, ns["cbc"] + "Name")
        name.text = self.company_id.name

    # An association to the Party that will really use the Inventory report(normally the branch for which the stock is reported).
    @api.model
    def _ubl_add_inventory_reporting_party(self, parent_node, ns, version="2.1"):
        '''
        Party
            PartyIdentification
                ID
            PartyName
                Name
            PostalAddress
                ID
                AddressLine
                    Line
        '''
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

    def _ubl_add_Additional_itemProperty(self, product, parent_node, ns):
        '''
        AdditionalItemProperty
            Name
            ValueQuantity
            ValueQualifier
        '''
        item = etree.SubElement(parent_node, ns["cac"] + "ItemProperty")
        valueQuantity = etree.SubElement(item, ns["cbc"] + "ValueQuantity")
        valueQuantity.text = str(product.list_price)
        valueQualifier = etree.SubElement(item, ns["cbc"] + "ValueQualifier")
        valueQualifier.text = product.cost_currency_id.name


    def _ubl_add_inventory_report_line(self, product, catalogue_line_id, parent_node, ns):
        '''
        ID
        Quantity
        AvailabilityDate
        AvailabilityStatusCode
        Item
            Description
            Name
            AdditionalItemProperty
        '''
        line_root = etree.SubElement(parent_node, ns["cac"] + "CatalogueLine")
        catalogue_id = etree.SubElement(line_root, ns["cbc"] + "ID")
        catalogue_id.text = str(catalogue_line_id)
        self._ubl_add_item(product, line_root, ns)
        self._ubl_add_itemProperty(product, line_root, ns)

    def generate_inventory_ubl_xml_etree(self, version="2.2"):
        nsmap, ns = self._ubl_get_nsmap_namespace("InventoryReport-2", version=version)
        xml_root = etree.Element("InventoryReport", nsmap=nsmap)
        self._ubl_add_header(xml_root, ns, version=version)

        self._ubl_add_retailer_customer_party(xml_root, ns)
        self._ubl_add_inventory_reporting_party(xml_root, ns)

        # Loop on the products in the catalogue
        catalogue_line_id = 0
        for product in self.item_ids:
            catalogue_line_id = catalogue_line_id + 1
            self._ubl_add_inventory_report_line(product, catalogue_line_id, xml_root, ns)

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