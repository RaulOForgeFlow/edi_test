# https://www.edureka.co/blog/python-xml-parser-tutorial/
# https://stackoverflow.com/questions/1912434/how-to-parse-xml-and-count-instances-of-a-particular-node-attribute

from odoo import models, fields, api, _
import datetime

class AccountMoveImport(models.TransientModel):
    _name = "account.move.import"
    _description = "Import Bills to Odoo"

    @api.model
    def parse_invoice(self, xml_root):
        vals = {}

        ################################################
        # PARSE THE ELEMENTS OF THE XML INVOICE-HEADER #
        ################################################
        invoice_header = xml_root.findall('Invoice-Header')

        for inv_head_fields in invoice_header:
            invoice_number = inv_head_fields.find('InvoiceNumber').text
            invoice_date_str = inv_head_fields.find('InvoiceDate').text
            invoice_currency = inv_head_fields.find('InvoiceCurrency').text
            invoice_payment_due_date_str = inv_head_fields.find('InvoicePaymentDueDate').text
            invoice_payment_terms = inv_head_fields.find('InvoicePaymentTerms').text
            customer_order_no = inv_head_fields.find('CustomerOrderNo').text
            vendor_number = inv_head_fields.find('VendorNumber').text

        invoice_currency_id = self.env['res.currency'].search([('name', '=', invoice_currency)]).id
        invoice_date = datetime.datetime.strptime(invoice_date_str, '%Y-%m-%d').date()
        invoice_payment_due_date = datetime.datetime.strptime(invoice_payment_due_date_str, '%Y-%m-%d').date()

        vals = {
            #'ref': invoice_number,
            'date': invoice_date,
            'invoice_date': invoice_date,
            'currency_id': invoice_currency_id,
            'invoice_date_due': invoice_payment_due_date,
            'state': 'draft',
            'type': 'in_invoice',
        }

        #############################################################
        # PARSE THE SEVERAL INVOICE PARTIES (Buyer. Payer & Seller) #
        #############################################################

        invoice_parties = xml_root.findall('Invoice-Parties')

        tax_id, register_number, name, street_and_number, city_name, country_name = [], [], [], [], [], []

        for party in invoice_parties[0]:
            tax_id.append(party.find('TaxID').text)
            register_number.append(party.find('RegisterNumber').text)
            name.append(party.find('Name').text)
            street_and_number.append(party.find('StreetAndNumber').text)
            city_name.append(party.find('CityName').text)
            country_name.append(party.find('CountryName').text)

        buyer_partner_id = self.env['res.partner'].search([('vat', '=', tax_id[0])]).id
        payer_partner_id = self.env['res.partner'].search([('vat', '=', tax_id[1])]).id
        seller_partner_id = self.env['res.partner'].search([('vat', '=', tax_id[2])]).id

        vals['partner_id'] = seller_partner_id

        ###################################
        # PARSE THE SEVERAL INVOICE-LINES #
        ###################################

        invoice_lines = xml_root.findall('Invoice-Lines')

        line_no, item_no, EAN, order_ref, order_ref2, order_ref3, inner_item_no, prod_description = [], [], [], [], [], [], [], []
        uom_code, quantity, unit_amount, line_amount, net_weight, gross_weight, currency_code, variant_code = [], [], [], [], [], [], [], []
        invoice_line_currency_id, purchase_orders_list = [], []
        purchase_orders_origin = ''

        # property_text should be defined as a matrix (each line a different invoice line & each column a different property_set)

        for invoice_line in invoice_lines[0]:
            line_no.append(invoice_line.find('LineNo').text)
            item_no.append(invoice_line.find('ItemNo').text)
            EAN.append(invoice_line.find('EAN').text)
            order_ref.append(invoice_line.find('OrderReference').text)
            order_ref2.append(invoice_line.find('OrderReference2').text)
            order_ref3.append(invoice_line.find('OrderReference3').text)
            inner_item_no.append(invoice_line.find('InnerItemNo').text)
            prod_description.append(invoice_line.find('ProductDescription').text)
            uom_code.append(invoice_line.find('UnitOfMeasureCode').text)
            quantity.append(invoice_line.find('Quantity').text)
            unit_amount.append(invoice_line.find('UnitAmount').text)
            line_amount.append(invoice_line.find('LineAmount').text)
            net_weight.append(invoice_line.find('NetWeight').text)
            gross_weight.append(invoice_line.find('GrossWeight').text)
            currency_code.append(invoice_line.find('CurrencyCode').text)
            variant_code.append(invoice_line.find('VariantCode').text)
            #property_sets = invoice_line.findall('PropertySet/PropertyText')
            #for set in property_sets:
            #    property_text.append(set.find('PropertyText').text)


            # Get the name of the different PO that are involved in the bill
            invoice_line_currency_id.append(self.env['res.currency'].search([('name', '=', currency_code[-1])]).id)
            if order_ref2 not in purchase_orders_list:
                purchase_orders_list.append(order_ref2[0][:-2])
                purchase_orders_origin += order_ref2[0][:-2] + ', '

            vals['invoice_origin'] = purchase_orders_origin[:-2]

        #########################################
        # PARSE THE INVOICE-SUMMARY INFORMATION #
        #########################################

        invoice_summary = xml_root.findall('Invoice-Summary')

        total_lines = invoice_summary[0].find('TotalLines').text
        total_inv_quantity = invoice_summary[0].find('TotalInvoiceQuantity').text
        total_net_amount = invoice_summary[0].find('TotalNetAmount').text
        total_tax_amount = invoice_summary[0].find('TotalTaxAmount').text
        total_gross_amount = invoice_summary[0].find('TotalGrossAmount').text

        ##########################################
        # CREATE THE ACCOUNT.MOVE RECORD IN ODOO #
        ##########################################

        account_move = self.env['account.move']
        account_move_record = account_move.create(vals)


        ###################################################
        # CREATE THE DIFFERENT ACCOUNT.MOVE.LINES IN ODOO #
        ###################################################

        account_move_line = self.env['account.move.line']
        account_move_line_ids = []

        for num_line in range(int(total_lines)):
            product = self.env['product.product'].search([('default_code', '=', item_no[num_line])])
            product31 = self.env['product.product'].search([('id', '=', 31)])
            account = product.property_account_expense_id

            line_vals = {
                'product_id': 31, #'product_id': product.id
                'name': order_ref2[num_line] + ': ' + prod_description[num_line],
                'account_id': product31.property_account_expense_id.id,
                'quantity': int(quantity[num_line]),
                'price_unit': float(unit_amount[num_line]),
                'currency_id': invoice_line_currency_id[num_line],
                'price_subtotal': float(line_amount[num_line]),
                'move_id': account_move_record.id,
            }
            account_move_line_ids.append(account_move_line.with_context(check_move_validity=False).create(line_vals).id)


        # Each account_move_line has an associated move_id/move_name, so a move called BNK/2021/0001 will have as
        # many lines as account_move_lines in the table with move_name BNK/2021/0001.

        # an account_move_line has a purchase_line_id field, which gives access to a purchase_order_line with fields as:
        # name, order_id, product_qty, product_id, qty_invoiced, qty_received, qty_received_manual

        # self.env['purchase.order'].search([('name','=', PO8352)])
        # account_move_line.purchase_line_id.name / .qty_received ...
        # self.env['purchase.order'].search([('id', '=', account_move_line.purchase_line_id.order_id)])

        # the invoice_origin char fields needs to be filled with all the purchase orders that are involved in the bill

        '''
        REQUIRED FIELDS IN ACCOUNT.MOVE
        - currency_id(many2one) - ----------------------------------------------- InvoiceCurrency
        - date(date) - ---------------------------------------------------------- InvoiceDate
        - extract_state(selection) - -------------------------------------------- done
            · no_extract_requested --> No extract requested
            · not_enough_credit --> Not enough credit
            · error_status --> An error occurred
            · waiting_extraction --> Waiting extraction
            · extract_not_ready --> waiting extraction, but it is not ready
            · waiting_validation --> Waiting validation
            · done --> Completed Flow
        - journal_id(many2one)
        - name(char)
        - state(selection) - ----------------------------------------------------- draft
            · draft --> Draft
            · posted --> Posted
            · cancelled --> Cancelled
        - type(selection) - ------------------------------------------------------ in_invoice
            · entry --> Journal Entry
            · out_invoice --> Customer Invoice
            · out_refund --> Customer Credit Note
            · in_invoice --> Vendor Bill
            · in_refund --> Vendor Credit Note
            · out_receipt --> Sales Receipt
            · in_receipt --> Purchase Receipt        
        '''

        '''
        process_mail()
        process_attatchment()
        create_invoice_from_attatchment()
            xml_content = etree.fromstring()
            for dte_xml in xml_content.xpath('//ns0:DTE', namespaces=XML_NAMESPACES):
                document_number = self._get_document_number(dte_xml)
                document_type_code = self._get_document_type_from_xml(dte_xml)
                issuer_vat = self._get_dte_issuer_vat(dte_xml)
                partner = self._get_partner(issuer_vat)
                
                with Form(self.env['account.move'].with_context(default_move_type=default_move_type, allowed_company_ids=[company_id],account_predictive_bills_disable_prediction=True)) as invoice_form:
                    invoice_form.partner_id = partner
                    invoice_form.invoice_source_email = from_address
                    
                    invoice_date = dte_xml.findtext('.//ns0:FchEmis', namespaces=XML_NAMESPACES)
                    if invoice_date is not None:
                        invoice_form.invoice_date = fields.Date.from_string(invoice_date)
                        
                    invoice_form.date = fields.Date.context_today(self.with_context(tz='America/Santiago'))
                
                    invoice_date_due = dte_xml.findtext('.//ns0:FchVenc', namespaces=XML_NAMESPACES)
                    if invoice_date_due is not None:
                        invoice_form.invoice_date_due = fields.Date.from_string(invoice_date_due)

                    journal = self._get_dte_purchase_journal(company_id)
                    if journal:
                        invoice_form.journal_id = journal

                    currency = self._get_dte_currency(dte_xml)
                    if currency:
                        invoice_form.currency_id = currency
                        
                    invoice_form.l10n_latam_document_type_id = document_type
                    invoice_form.l10n_latam_document_number = document_number
                    
                    for invoice_line in self._get_dte_lines(dte_xml, company_id, partner.id):
 
                    
                    
                    def _get_dte_lines():
                         invoice_lines = []
                         for dte_line in dte_xml.findall('.//ns0:Detalle', namespaces=XML_NAMESPACES):
                            product_code = dte_line.findtext('.//ns0:VlrCodigo', namespaces=XML_NAMESPACES)
                            product_name = dte_line.findtext('.//ns0:NmbItem', namespaces=XML_NAMESPACES)
                            product = self._get_vendor_product(product_code, product_name, company_id, partner_id)
                            quantity = float(dte_line.findtext('.//ns0:QtyItem', default=1, namespaces=XML_NAMESPACES))
                            price_unit = float(dte_line.findtext('.//ns0:PrcItem', default=dte_line.findtext('.//ns0:MontoItem', namespaces=XML_NAMESPACES), namespaces=XML_NAMESPACES))
                        
                            values = {
                                'product': product,
                                'name': product.name if product else dte_line.findtext('.//ns0:NmbItem', namespaces=XML_NAMESPACES),
                                'quantity': quantity,
                                'price_unit': price_unit,
                                'discount': float(dte_line.findtext('.//ns0:DescuentoPct', default=0, namespaces=XML_NAMESPACES)),
                                'default_tax': False
                            }
                            
                            if (dte_xml.findtext('.//ns0:TasaIVA', namespaces=XML_NAMESPACES) is not None and dte_line.findtext('.//ns0:IndExe', namespaces=XML_NAMESPACES) is None):
                                values['default_tax'] = True
                                values['taxes'] = self._get_withholding_taxes(company_id, dte_line)
                            invoice_lines.append(values)
                            
                    
                    
                    
                    def _get_vendor_product(self, product_code, product_name, company_id, partner_id):
        
                        if partner_id:
                            supplier_info_domain = [('name', '=', partner_id), ('company_id', 'in', [company_id, False])]
                            if product_code:
                                # 1st criteria
                                supplier_info_domain.append(('product_code', '=', product_code))
                            else:
                                # 2nd criteria
                                supplier_info_domain.append(('product_name', '=', product_name))
                            supplier_info = self.env['product.supplierinfo'].sudo().search(supplier_info_domain, limit=1)
                            if supplier_info:
                                return supplier_info.product_id
                        # 3rd criteria
                        if product_code:
                            product = self.env['product.product'].sudo().search([
                                '|', ('default_code', '=', product_code), ('barcode', '=', product_code),
                                ('company_id', 'in', [company_id, False]), ], limit=1)
                            if product:
                                return product
                        # 4th criteria
                        return self.env['product.product'].sudo().search([
                            ('company_id', 'in', [company_id, False]), ('name', 'ilike', product_name)], limit=1)
        '''