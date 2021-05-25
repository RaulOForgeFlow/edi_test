import xml.etree.ElementTree as ET

def parse_xml():
    root = ET.parse('/home/ferran/odoo-dev13/edi_test/TXD037547.xml').getroot()
    # https://www.edureka.co/blog/python-xml-parser-tutorial/
    # https://stackoverflow.com/questions/1912434/how-to-parse-xml-and-count-instances-of-a-particular-node-attribute

    #Parse the elements of the Invoice-Header
    invoice_header = root.findall('Invoice-Header')

    for inv_head_fields in invoice_header:
         invoice_number = inv_head_fields.find('InvoiceNumber').text
         invoice_date = inv_head_fields.find('InvoiceDate').text
         invoice_currency = inv_head_fields.find('InvoiceCurrency').text
         invoice_payment_due_date = inv_head_fields.find('InvoicePaymentDueDate').text
         invoice_payment_terms = inv_head_fields.find('InvoicePaymentTerms').text
         customer_order_no = inv_head_fields.find('CustomerOrderNo').text
         vendor_number = inv_head_fields.find('VendorNumber').text

    # Parse the several invoice parties of the Invoice-Parties (Buyer, Seller & Payer)
    invoice_parties = root.findall('Invoice-Parties')

    tax_id, register_number,  name,  street_and_number,  city_name, country_name = [],[],[],[],[],[]

    for party in invoice_parties[0]:
        tax_id.append(party.find('TaxID').text)
        register_number.append(party.find('RegisterNumber').text)
        name.append(party.find('Name').text)
        street_and_number.append(party.find('StreetAndNumber').text)
        city_name.append(party.find('CityName').text)
        country_name.append(party.find('CountryName').text)

    # Parse the several invoice lines of the Invoice-Lines
    invoice_lines = root.findall('Invoice-Lines')

    line_no, item_no, EAN, order_ref, order_ref2, order_ref3, inner_item_no, prod_description = [],[],[],[],[],[],[],[]
    uom_code, quantity, unit_amount, line_amount, net_weight, gross_weight, currency_code, variant_code = [],[],[],[],[],[],[],[]

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

        '''
        property_sets = invoice_line.findall('PropertySet/PropertyText')
        for set in property_sets:
            property_text.append(set.find('PropertyText').text)
        '''

    # Parse the Invoice-Summary information
    invoice_summary = root.findall('Invoice-Summary')

    total_lines = invoice_summary.find('TotalLines').text
    total_inv_quantity = invoice_summary.find('TotalInvoiceQuantity').text
    total_net_amount = invoice_summary.find('TotalNetAmount').text
    total_tax_amount = invoice_summary.find('TotalTaxAmount').text
    total_gross_amount = invoice_summary.find('TotalGrossAmount').text


if (__name__ == "__main__"):
    parse_xml()
    '''
    Document-Invoice - account.move
        Invoice-Header
            InvoiceNumber - account.move.ref
            InvoiceDate - account.move.invoice_date
            InvoiceCurrency - 
            InvoicePaymentDueDate -
            InvoicePaymentTerms - account.move.invoice_payment_term_id
            CustomerOrderNo - 
            VendorNumber - 
        Invoice-Parties
            Buyer, Payer, Seller
                TaxID - res.partner
                RegisterNumber -
                Name - res.partner.name
                StreetAndNumber - res.partner.street
                CityName - res.partner.city
                CountryNames - res.partner.country_id
        Invoice-Lines
            InvoiceLine account_move.invoice_line_ids
                LineNo
                ItemNo
                EAN
                OrderReference "their SO reference"
                OrderReference2 "their PO reference"
                OrderReference3 ""
                InnerItemNo product.product.default_code // product.product.item_number
                
                ProductDescription
                UnitOfMeasureCode
                Quantity - quantity
                UnitAmount - price_unit
                LineAmount - price_subtotal
                NetWeight
                GrossWeight
                CurrencyCode
                VariantCode
                PropertySet
                    PropertyText
        Invoice-Summary
            TotalLines - len(invoice_line_ids)
            TotalInvoiceQuantity - account.move.amount_total
            TotalNetAmount - account.move.amount_untaxed
            TotalTaxAmount - account.move.amount_by_group
            TotalGrossAmount - account.move.amount_residual
            
            
    REQUIRED FIELDS IN ACCOUNT.MOVE
                    - currency_id (many2one) ------------------------------------------------ InvoiceCurrency
                    - date (date) ----------------------------------------------------------- InvoiceDate
                    - extract_state (selection) --------------------------------------------- done
                        · not_extract_requested --> NO extract requested
                        · not_enough_credit --> Not enough credit
                        · error_status --> An error occurred
                        · waiting_extraction --> Waiting extraction
                        · extract_not_ready --> waiting extraction, but it is not ready
                        · waiting_validation --> Waiting validation
                        · done --> Completed Flow            
                    - journal_id (many2one)
                    - name (char)
                    - state (selection) ------------------------------------------------------ draft
                        · draft --> Draft
                        · posted --> Posted
                        · cancelled --> Cancelled
                    - type (selection) ------------------------------------------------------- in_invoice
                        · entry --> Journal Entry
                        · out_invoice --> Customer Invoice
                        · out_refund --> Customer Credit Note
                        · in_invoice --> Vendor Bill
                        · in_refund --> Vendor Credit Note
                        · out_receipt --> Sales Receipt 
                        · in_receipt --> Purchase Receipt
        '''
