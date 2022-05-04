from odoo import api, fields, models
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools import float_compare

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "estate property offer"
    _order = "price desc"

    name = fields.Char('Property offer')
    price = fields.Float('Price', default=1)
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False)
    
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    property_type_id = fields.Many2one(related='property_id.estate_property_type_id', store=True)
    

    validaty = fields.Integer('Validaty(days)', default=7)
    create_date = fields.Date('Сreate Date')
    date_deadline = fields.Date('Deadline', compute="_compute_deadline", inverse="_inverse_deadline")

    @api.depends('create_date', 'validaty')
    def _compute_deadline(self):
        with open('/tmp/log', 'a') as f:
            f.write('_compute_deadline')
        for record in self:
            if not record.create_date:
                record.create_date = None
            else:
                record.date_deadline = record.create_date+timedelta(days=record.validaty)

    def _inverse_deadline(self):
        with open('/tmp/log', 'a') as f:
            f.write('_inverse_deadline')
        for record in self:
            if not record.create_date:
                record.create_date = None
            if not record.date_deadline:
                record._compute_deadline()
            else:
                validaty_1 = record.date_deadline-record.create_date
                record.validaty = validaty_1.days
    
    def action_refused(self):
        self.status ="refused"

    def action_accepted(self):
        for offer in self.property_id.offer_ids:
            if offer.status == "accepted":
                raise UserError ("Another offer have been accepted!")
        self._check_price()
        self.status ="accepted"
        self.property_id.state = 'offer accepted'

    def action_offers(self):
        self.property_id.offer_ids

    @api.constrains('property_id', 'price')
    def _check_price(self):
        percent = self.property_id.expected_price - (self.property_id.expected_price/10)
        if float_compare(self.price, percent, precision_digits=1) >= 0:
            return True
        else:
            raise ValidationError("Selling Price should'nt be lower over 10% ")


    _sql_constraints = [
        ('price', 'CHECK(price >= 0)', 'The price should be over 0.')
        ]

    @api.model
    def create(self,vals):
        current_property = self.env['estate.property'].browse(vals['property_id'])
        if vals['price'] < current_property.best_offer:
            raise ValidationError("Offers Price should'nt be lower then price in other offers{self.price}")
        current_property.state = 'offer received'

        return super(EstatePropertyOffer, self).create(vals)