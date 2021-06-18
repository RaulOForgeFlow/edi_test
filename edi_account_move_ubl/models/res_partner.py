from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    account_import = fields.One2many(
        "account.move.import", "invoice_company", "Account Move Import selection"
    )
    ftp_subdirectory = fields.Char("File inside the FTP directory")
