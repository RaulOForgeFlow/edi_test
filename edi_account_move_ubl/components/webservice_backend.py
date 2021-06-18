from odoo import fields, models


class WebServiceBackend(models.Model):

    _inherit = "webservice.backend"

    protocol = fields.Selection(
        selection_add=[("sftpInvoice", "SFTP Invoices")], store=True
    )
    ftpDirectory = fields.Char(string="FTP Directory", required=True)
