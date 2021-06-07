import base64
import logging
import datetime

from lxml import etree

from odoo.tests import Form
from odoo import api, fields, models, tools, _

_logger = logging.getLogger(__name__)

class AccountMoveImport(models.TransientModel):
    _name = "account.move.import"
    _description = "Import Bills to Odoo"


    def create_invoice_from_attachment(self, xml_root):
        moves = []

        invoice_header = xml_root.findall('Invoice-Header')
        for inv_head_fields in invoice_header:
            invoice_number = inv_head_fields.find('InvoiceNumber').text
            invoice_date_str = inv_head_fields.find('InvoiceDate').text
            invoice_currency = inv_head_fields.find('InvoiceCurrency').text
            invoice_payment_due_date_str = inv_head_fields.find('InvoicePaymentDueDate').text
            invoice_payment_terms = inv_head_fields.find('InvoicePaymentTerms').text
            customer_order_no = inv_head_fields.find('CustomerOrderNo').text
            vendor_number = inv_head_fields.find('VendorNumber').text

        invoice_form, invoice_origin = self._get_invoice_form(xml_root, invoice_number, invoice_date_str, invoice_currency, invoice_payment_due_date_str)

        move = invoice_form.save()

        move.write({
            'invoice_origin': invoice_origin
        })

        dte_attachment = self.env['ir.attachment'].create({
            'name': 'DTE_{}.xml'.format(invoice_number),
            'res_model': self._name,
            'res_id': move.id,
            'type': 'binary',
            'datas': base64.b64encode(etree.tostring(xml_root))
        })
        move.l10n_cl_dte_file = dte_attachment.id
        moves.append(move)

        return moves

    def _get_invoice_form(self, xml_root, invoice_number, invoice_date_str, invoice_currency, invoice_payment_due_date_str):

        with Form(self.env['account.move'].with_context(default_type='in_invoice')) as invoice_form:

            # Invoice reference number
            invoice_form.ref = invoice_number

            # Invoice date and invoice due date
            invoice_date = datetime.datetime.strptime(invoice_date_str, '%Y-%m-%d').date()
            invoice_payment_due_date = datetime.datetime.strptime(invoice_payment_due_date_str, '%Y-%m-%d').date()

            if invoice_date is not None:
                invoice_form.invoice_date = invoice_date
            if invoice_payment_due_date is not None:
                invoice_form.invoice_date_due = invoice_payment_due_date

            # Invoice currency
            currency = self.env['res.currency'].search([('name', '=', invoice_currency)])
            if currency:
                invoice_form.currency_id = currency

            # Invoice journal
            journal = self.env['account.journal'].search([('type', '=', 'purchase'), ('company_id', '=', self.company_id.id)], limit=1)
            if journal:
                invoice_form.journal_id = journal

            # Invoice vendor
            seller_party = xml_root.findall('Invoice-Parties/Seller')
            for party in seller_party:
                tax_id = party.find('TaxID').text
            seller_partner = self.env['res.partner'].search([('vat', '=', tax_id)])
            seller_partner.ensure_one()

            seller_partner = self.env['res.partner'].search([('name', '=', 'Azure Interior')])
            invoice_form.partner_id = seller_partner

            purchase_references = []

            # Invoice lines
            for invoice_line in self._get_dte_lines(xml_root):
                with invoice_form.invoice_line_ids.new() as invoice_line_form:
                    product = invoice_line.get('product', self.env['product.product'])
                    invoice_line_form.product_id = product
                    invoice_line_form.name = invoice_line.get('name')
                    invoice_line_form.account_id = invoice_line.get('account_id', self.env['account.account'])
                    invoice_line_form.quantity = invoice_line.get('quantity')
                    invoice_line_form.price_unit = invoice_line.get('price_unit')

                    purchase_references.append(invoice_line.get('purchase_reference').split("-")[0])
                    po_id = self.env['purchase.order'].search([('name', '=', purchase_references[-1].split("-")[0])]).id
                    po_lines = self.env['purchase.order.line'].search([('order_id', '=', po_id)])
                    for po_line in po_lines:
                        if po_line.product_id.id == product.id:
                            purchase_order_line = po_line
                            invoice_line_form.purchase_line_id = purchase_order_line

            # Invoice purchase origin
            invoice_origin = ''
            for reference in purchase_references:
                if reference not in invoice_origin:
                    invoice_origin += reference + ', '

            # references are defined P0003-1, need to delete the -1 with [:-2] or split it by the - sign
            return invoice_form, invoice_origin[:-2]

    def _get_dte_lines(self, xml_root):
        """
        This parses DTE invoice detail lines and tries to match lines with existing products.
        If no products are found, it puts only the description of the products in the draft invoice lines
        """
        invoice_lines = []
        xml_invoice_lines = xml_root.findall('Invoice-Lines')

        for invoice_line in xml_invoice_lines[0]:
            product_code = invoice_line.find('ItemNo').text
            product_name = invoice_line.find('ProductDescription').text
            purchase_reference = invoice_line.find('OrderReference2').text
            product = self.env['product.product'].search([('default_code', '=', product_code)])
            quantity = float(invoice_line.find('Quantity').text)
            price_unit = float(invoice_line.find('UnitAmount').text)
            price_line = float(invoice_line.find('LineAmount').text)
            account_id = product.property_account_expense_id

            values = {
                'product': product,
                'name': product.name,
                'purchase_reference': purchase_reference,
                'quantity': quantity,
                'price_unit': price_unit,
                'default_tax': False,
                'account_id': account_id,
                'tax_ids': 5
            }
            invoice_lines.append(values)

        return invoice_lines






