from odoo import models, fields, api, _
from ..scripts.num_files_ftp import count_files
from odoo.exceptions import UserError

class AccountMoveWizard(models.TransientModel):
    _name = 'account.move.import'
    _description = "Wizard for Account Moves UBL"
    _inherit = ["account.move.import", "account.move", "edi.exchange.consumer.mixin"]

    name = fields.Char(required=False)
    date = fields.Date(required=False)
    state = fields.Selection(required=False)
    type = fields.Selection(required=False)
    journal_id = fields.Many2one(required=False)
    currency_id = fields.Many2one(required=False)
    extract_state = fields.Selection(required=False)

    # Overwrite transaction_ids field modifying the table where relations are stored so not to crash with original
    transaction_ids = fields.Many2many('payment.transaction', 'account_move_transaction_rel', 'invoice_id',
                                       'transaction_id', string='Transactions', copy=False, readonly=True)

    def receive_invoice_button(self):
        '''
        files_FTP = count_files('invoices')
        num_files = len(files_FTP)

        if num_files == 0:
            raise UserError("There are no files to receive in the FTP server. Please upload first at least one")
        else:
            # Update and receive all the sales at once
            for rep in range(num_files):
                self._event("on_get_invoice").notify(self)
        '''

        self._event("on_get_invoice").notify(self)