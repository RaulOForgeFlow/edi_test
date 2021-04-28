# Copyright 2014-2015 Grupo ESOC <www.grupoesoc.es>
# Copyright 2017-Apertoso N.V. (<http://www.apertoso.be>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': "My Library",
    'summary': "Manage books easily",
    'version':'13.0.0.0.0',
    'depends': ['base','edi','edi_webservice'],
    'data': [
        'data/data.xml',
        'views/library_book.xml',
        'security/groups.xml',
        'security/ir.model.access.csv',
        'wizards/library_book_wizard.xml',
    ],
    'demo':['data/demo.xml'],
    "qweb": ["static/src/xml/widget_edi.xml"],
}