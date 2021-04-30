from odoo import models, fields, api, _
from ..scripts.num_files_ftp import count_files
from odoo.exceptions import UserError

class SaleOrderWizard(models.TransientModel):
    _name = "sale.order.wizard"
    _description = "Wizard for Sale Orders UBL"
    _inherit = ["sale.order", "edi.exchange.consumer.mixin"]

    # Overwrite the required fields as non-required (name, date_order, partner_id...)
    name = fields.Char(required=False)
    date_order = fields.Datetime(required=False)
    partner_id = fields.Many2one(required=False)
    partner_invoice_id = fields.Many2one(required=False)
    partner_shipping_id = fields.Many2one(required=False)
    pricelist_id = fields.Many2one(required=False)
    currency_id = fields.Many2one(required=False)
    company_id = fields.Many2one(required=False)
    order_id = fields.Many2one(required=False)

    # Overwrite transaction_ids field modifying the table where relations are stored so not to crash with original
    transaction_ids = fields.Many2many('payment.transaction', 'sale_order_wizard_transaction_rel', 'sale_order_id',
                                       'transaction_id',
                                       string='Transactions', copy=False, readonly=True)


    def receive_sale_button(self):
        files_FTP = count_files('purchases')
        num_files = len(files_FTP)

        if num_files == 0:
            raise UserError("There are no files to receive in the FTP server. Please upload first at least one")
        else:
            # Update and receive all the sales at once
            for rep in range(num_files):
                self._event("on_get_sale").notify(self)