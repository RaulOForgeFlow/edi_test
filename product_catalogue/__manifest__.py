# Copyright 2014-2015 Grupo ESOC <www.grupoesoc.es>
# Copyright 2017-Apertoso N.V. (<http://www.apertoso.be>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': "Product Catalogue",
    'summary': "Generate different product catalogues for different partners",
    'version':'13.0.0.0.0',
    'depends': ['base','product'],
    'data': [
        'views/product_catalogue.xml',
        'views/res_partner.xml',
        'security/groups.xml',
        'security/ir.model.access.csv',
    ],
    'demo':[],
    "qweb": [],
}