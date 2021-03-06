# © 2016-2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# Copyright 2020 Onestein (<https://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
from lxml import etree
from odoo import api, fields, models

logger = logging.getLogger(__name__)


class Product(models.Model):
    _name = "stock.picking"
    _inherit = ["stock.picking", "base.ubl"]


    # Should work with move_lines
    def _ubl_add_delivery(self, parent_node, ns,):
        scheduled_date = etree.SubElement(parent_node, ns["cbc"] + "ActualDeliveryDate")
        scheduled_date.text = str(self.scheduled_date)
        address = etree.SubElement(parent_node, ns["cac"] + "DeliveryAddress")
        address_line = etree.SubElement(address, ns["cac"] + "AddressLine")
        line = etree.SubElement(address_line, ns["cbc"] + "Line")
        line.text = self.partner_id.contact_address



    def _ubl_add_goods_item(self, product, parent_node, ns, version="2.1"):

        item = etree.SubElement(parent_node, ns["cac"] + "Item")

        id = etree.SubElement(item, ns["cbc"] + "ID")
        id.text = str(product.product_tmpl_id.id)

        name = etree.SubElement(item, ns["cbc"] + "Name")
        name.text = product.product_tmpl_id.name

        #quantity = etree.SubElement(parent_node, ns["cbc"] + "Quantity")
        #quantity.text = str(self.move_line_ids.qty_done)

    def _ubl_add_header(self, parent_node, ns, version="2.1"):
        now_utc = fields.Datetime.to_string(fields.Datetime.now())
        date = now_utc[:10]
        ubl_version = etree.SubElement(parent_node, ns["cbc"] + "UBLVersionID")
        ubl_version.text = version
        doc_id = etree.SubElement(parent_node, ns["cbc"] + "ID")
        doc_id.text = self.name
        issue_date = etree.SubElement(parent_node, ns["cbc"] + "IssueDate")
        issue_date.text = date
        name = etree.SubElement(parent_node, ns["cbc"] + "Name")
        name.text = self.name


    def _ubl_add_shipment(self, parent_node, ns):
        line_root = etree.SubElement(parent_node, ns["cac"] + "Shipment")

        shipment_id = etree.SubElement(line_root, ns["cbc"] + "ID")
        shipment_id.text = str(self.id)
        weight = etree.SubElement(line_root, ns["cbc"] + "NetWeightMesure")
        weight.text = str(self.weight)

        # make the relation with stock.move.line since
        for line in self.move_lines:
            self._ubl_add_goods_item(line, line_root, ns)
            # The following info can be taken from product
            # image_1024(b), invoice_policy(str), lst_price(float), name(str), partner_ref(str), product_tmpl_id, weight(float), weight_uom_name(str)
            # aspects that should be added currencyID='USD'>1000.0 (cost_currency_id.name, cost_currency_id.rate) && unitCode='C62'>1 (self.move_lines.product_uom.unece_code)
            # self.backorder_id

        self._ubl_add_delivery(line_root, ns)


    def generate_shipping_ubl_xml_etree(self, version="2.1"):
        nsmap, ns = self._ubl_get_nsmap_namespace("PackingList-2", version=version)
        xml_root = etree.Element("PackingList", nsmap=nsmap)
        self._ubl_add_header(xml_root, ns, version=version)
        '''
        attributes = self.move_lines.move_line_ids.product_id.product_variant_id.product_template_attribute_value_ids
        for attribute in attributes:
            attribute.display_name #Legs_Aluminium
            attribute.name #Aluminium
            attribute.attribute_id.name #Legs
        '''
        self._ubl_add_shipment(xml_root, ns)

        return xml_root

        '''
        Shipment
            ID
            NetWeightMesure
            GoodsItem
                ID
                Quantity
                Item
                   Name 
            Delivery
                ID self.id
                Actual Delivery Date self.scheduled_date
                Delivery Address self.partner_id.contact_address
                DeliveryParty
                Carrier Party
                
                
                
                self.carrier_id
                    self.carrier_id.name
                    self.delivery_type (dhl, base_on_rule)
                    tracking reference???
                self.carrier_price
                self.has_tracking
                self.carrier_tracking_ref
                self.delivery_type (fixed_price, based_on_rules, dhl)
                self.display_name(WH/OUT/00019)
                self.message_partner_ids (res.partner)
                
                self.move_lines
                    self.name '[DESK0005] Customizable Desk (CONFIG) (Custom, White) 160x80cm, with large legs.'
                    self.description_pìcking('Customizable Desk (CONFIG)')
                    self.product_quantity
                    self.move_line_ids
                          self.display_name([DESK0005] Customizable Desk (CONFIG) (Custom, White))
                          self.product_id
                            self.code(DESK0005)
                            self.description_sale('160x80cm, with large legs.') ¡¡¡MAY BE FALSE!!!
                            self.cost_currency_id
                            self.display name / name (USD)
                            self.list_price
                            self.partner_ref([DESK0005] Customizable Desk (CONFIG) (Custom, White)')
                            self.product_variant_count
                            self.product_template_attribute_value_ids
                                self.display_name (Legs_Aluminium)
                                self.name (Aluminium)
                                self.attribute_id.name (Legs)
                            
                self.origin(S00027)
                self.partner_id
                self.sale_id
                self.location_dest_id (stcok.location)
                self.location_id (stock.location)
                self.state
                self.weight_bulk(0.01)
                self.weight_uom_name(kg)
                
        '''