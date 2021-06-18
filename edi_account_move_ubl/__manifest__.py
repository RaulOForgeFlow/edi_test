# Copyright 2021 ForgeFlow, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "EDI Account UBL",
    "summary": "EDI Exchange with UBL format",
    "version": "13.0.1.0.0",
    "license": "AGPL-3",
    "author": "ForgeFlow",
    "depends": [
        "base",
        "edi",
        "edi_webservice",
        "account_move_import_ltp",
        "account_invoice_ubl",
    ],
    "data": [
        "data/data.xml",
        "views/account_move.xml",
        "views/webservice_backend.xml",
        "views/res_partner.xml",
        "wizards/account_move_import.xml",
    ],
    "demo": [],
}
