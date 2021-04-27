# Copyright 2014-2015 Grupo ESOC <www.grupoesoc.es>
# Copyright 2017-Apertoso N.V. (<http://www.apertoso.be>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': "EDI Pucrhase Order UBL",
    'summary': "EDI Exchange with UBL format",
    'version':'13.0.0.0.0',
    'depends': ['base','edi','edi_webservice', 'purchase_order_ubl'],
    'data': ['data/data.xml', 'views/purchase_order.xml'],
    'demo':[],
}