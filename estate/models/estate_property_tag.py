from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tags of estate property"
    _order = "name"

    name = fields.Char('Property tags', required=True)
    color = fields.Integer("Color")
    _sql_constraints = [
        ('name', 'UNIQUE(name)', 'Tags name should be unique')
    ]
