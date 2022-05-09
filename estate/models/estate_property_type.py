from odoo import api, fields, models
from dateutil.relativedelta import relativedelta

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of estate property"
    _order = "sequence, name"

    sequence = fields.Integer('Sequence')
    name = fields.Char('Property type', required=True)
    description = fields.Char()
    property_ids = fields.One2many("estate.property", "estate_property_type_id")
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer("offer_count", compute='_compute_offers') 

    _sql_constraints = [
        ('name', 'UNIQUE(name)', 'Property type should be unique')
    ]

    @api.depends('offer_ids')
    def _compute_offers(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
