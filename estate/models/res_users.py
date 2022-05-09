from odoo import models, fields

class Users(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many('estate.property', 'seller_id', 
    	domain=[('state', '!=', 'canceled'), ('state', '!=', 'offer accepted'), ('state', '!=', 'sold')])