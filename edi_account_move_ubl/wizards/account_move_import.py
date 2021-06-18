import ftplib

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountMoveWizard(models.TransientModel):
    _name = "account.move.import"
    _description = "Wizard for Account Moves UBL"
    _inherit = ["account.move.import", "account.move", "edi.exchange.consumer.mixin"]

    # Redefine all the required fields in the account.move model as not required
    name = fields.Char(required=False)
    date = fields.Date(required=False)
    state = fields.Selection(required=False)
    type = fields.Selection(required=False)
    journal_id = fields.Many2one(required=False)
    currency_id = fields.Many2one(required=False)
    extract_state = fields.Selection(required=False)

    # Overwrite transaction_ids field modifying the table where
    # relations are stored so not to crash with original
    transaction_ids = fields.Many2many(
        "payment.transaction",
        "account_move_transaction_rel",
        "invoice_id",
        "transaction_id",
        string="Transactions",
        copy=False,
        readonly=True,
    )

    # Define a new many2one res.partner field to select in the prompting wizard
    invoice_company = fields.Many2one("res.partner", "Company to invoice")

    def receive_invoice_button(self):

        webservice_backend = self.env["webservice.backend"].search(
            [("code", "=", "invoice")]
        )

        ftp_subdirectory = self.invoice_company.ftp_subdirectory = "ltp"
        # ftp_subdirectory = self.invoice_company.ftp_subdirectory

        if not ftp_subdirectory:
            raise UserError(_("There is no FTP subdirectory set for this company"))
        else:
            files_FTP = self.count_files(webservice_backend, ftp_subdirectory)
            num_files = len(files_FTP)

            if num_files == 0:
                raise UserError(
                    _(
                        "There are no files to receive in the FTP server. "
                        "Please upload first at least one"
                    )
                )
            else:
                # Update and receive all the sales at once
                for _rep in range(num_files):
                    self._event("on_get_invoice").notify(self)

    @api.model
    def count_files(self, webservice_backend, ftp_subdirectory):

        url = webservice_backend.server_env_defaults["url_env_default"]
        user = webservice_backend.server_env_defaults["username_env_default"]
        password = webservice_backend.server_env_defaults["password_env_default"]

        directory = webservice_backend.ftpDirectory + "/" + ftp_subdirectory

        session = ftplib.FTP(url, user, password)
        session.cwd(directory)
        files = session.nlst()
        return files
