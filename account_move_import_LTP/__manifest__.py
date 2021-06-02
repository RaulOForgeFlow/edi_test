# © 2015-2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Account Move Import',
    'version': '13.0.1.0.0',
    'category': 'Accounting & Finance',
    'license': 'AGPL-3',
    'summary': 'Import supplier invoices/refunds as XML files LTP formatted based',
    'website': 'https://github.com/OCA/edi',
    'depends': [
        'account',
        'base_iban',
        'base_business_document_import',
        'onchange_helper',
        'base_ubl',
        ],
    'data': [],
    'installable': True,
}
