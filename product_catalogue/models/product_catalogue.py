from odoo import api, fields, models, tools, _

class ProductCatalogue(models.Model):
    _name = "product.catalogue"
    _description = "Product Catalogue"

    name = fields.Char('Catalogue Name', required=True, translate=True)
    item_ids = fields.Many2many('product.product', string='Catalogue Items') #product_catalogue_product_product_rel
    partner_id = fields.One2many('res.partner', 'catalogue_id', string='Partner')
    company_id = fields.Many2one('res.company', 'Company')



class ResPartner(models.Model):
    _inherit = 'res.partner'

    catalogue_id = fields.Many2one('product.catalogue', string='Catalogue')

    def get_catalogue(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Catalogue',
            'view_mode': 'tree',
            'res_model': 'product.catalogue',
            'domain': [('partner_id', '=', self.id)],
            'context': "{'create': False}",
        }

'''
class CatalogueItem(models.Model):
    _inherit = 'product.product'

    catalogue_id = fields.Many2one('product.catalogue', 'Catalogue')
'''
'''
class CatalogueItem(models.Model):
    _name = "product.catalogue.item"
    _description = "Catalogue Rule"

    name = fields.Char('Name', help="Explicit rule name for this catalogue line")
    catalogue_id = fields.Many2one('product.catalogue', 'Catalogue')

    company_id = fields.Many2one('res.company', 'Company')

    product_tmpl_id = fields.Many2one('product.template', 'Product')
    product_id = fields.Many2one('product.product', 'Product Variant')
'''

