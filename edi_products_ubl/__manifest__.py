# © 2016-2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "EDI Product Catalogue UBL",
    "version": "13.0.1.0.0",
    "category": "Product",
    "license": "AGPL-3",
    "summary": "Exchange product catalogues in UBL format",
    "author": "Ferran Coll, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/edi/",
    'depends': ['base','edi','edi_webservice', 'product_ubl'],
    "data": ["views/product.xml", "data/data.xml"],
}
