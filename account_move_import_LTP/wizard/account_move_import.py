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
                'quantity': quantity[num_line],
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