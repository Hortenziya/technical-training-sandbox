from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import AccessError, UserError, ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Quantity and Quality estate property"
    _order = 'id desc'

    active = fields.Boolean('Active', default=True)
    state = fields.Selection(string='State', required=True, copy=False,
            selection=[
            ('new', 'New'), 
            ('offer received', 'Offer Received'),
            ('offer accepted', 'Offer Accepted'),
            ('sold','Sold'), 
            ('canceled','Canceled')
            ],
            default='new')
    
    name = fields.Char('Property name', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Available From', default=lambda self: fields.Datetime.now()+relativedelta(months=3), copy=False)
    expected_price = fields.Float('Expected price', required=True)
    selling_price = fields.Float('Selling price', readonly=True, copy=False, compute='_compute_accepted')
    bedrooms = fields.Integer('Rooms', default=2)
    living_area = fields.Integer('Living area(sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden area(sqm)')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="Garden Orientation is not defind")
    other_info = fields.Text('Other Info')
    estate_property_type_id = fields.Many2one("estate.property.type", string="Property type")
    company_id = fields.Many2one('res.company', string="Company", required=True)
    buyer_id = fields.Many2one('res.partner', copy=False, string="Buyer", compute='_compute_accepted')
    seller_id = fields.Many2one('res.users', string="Salesman", default=lambda self: self.env.user)
    estate_property_tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    total_area = fields.Char(compute="_compute_area")
    best_offer = fields.Float(compute="_compute_offer")

    
    # визначеня загальної площі
    @api.depends('living_area', 'garden_area')
    def _compute_area(self):
        for record in self:
            record.total_area = record.living_area+record.garden_area
    
    # визначення офера із набільшою ціною, якщо немає значення - значення None
    @api.depends('offer_ids')
    def _compute_offer(self):
        for record in self:
            offer_prices = record.offer_ids.mapped("price")
            if not offer_prices:
                record.best_offer = None
            else:
                record.best_offer = max(offer_prices)

    # якщо функція get_accepted_offer поверне, що прийнятий офер є, призначити в поля покупця його айді та 
    # в поле ціна продажі = ціну в цьому офері, а статус проперті поставити = офер прийнятий
    @api.onchange('offer_ids', 'offer_ids.status')
    def _compute_accepted(self):
        for record in self:
            offer = record.get_accepted_offer()
            if  offer:
                record.buyer_id = offer.partner_id
                record.selling_price = offer.price  
            if not offer:
                record.buyer_id = None
                record.selling_price = None
                
# якщо в проперті є сад, його положення ставиться на північ, площа - на 10
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_orientation = "north"
            self.garden_area = 10
        else:
            self.garden_orientation = None
            self.garden_area = None


# відмінити проперті. Однак,кщо проперті уже продано, то відмінити не можна 
    def action_cancel(self):
        if self.state == "sold":
            raise UserError("Sold Properties can't be canceled!")
        else:
            self.state = "canceled"
# продати проперті. якщо проперті відмінена - продати не можливо
    def action_sold(self):
        if self.state == "canceled":
            raise UserError("Canceled Properties can't be sold!")
        else:
           self.state = "sold"
# якщо є прийняти офер в списку оферів відкритого проперті - повернути прийнятий офер. якщо умова не виконалась - повернути None
    @api.returns('estate.property.offer')
    def get_accepted_offer(self):
        for offer in self.offer_ids:
            if offer.status == 'accepted':
                return offer
        return None

    @api.onchange("offer_ids")
    def _compute_state(self):
        if self.state == 'sold':
            return

        if len(self.offer_ids) == 0:
            self.state = 'new'
        else:
            offer = self.get_accepted_offer()
            if offer is not None:
                self.state = 'offer accepted'

    _sql_constraints = [
        ('expected_price', 'CHECK(expected_price >= 0)', 'The expected price should be over 0.')
        ]

    @api.ondelete(at_uninstall=False)
    def _unlink_delete_property(self):
        for record in self:
            if record.state in ("new", "canceled"):
                return True
            else:
                raise UserError("Can't delete Estate with such state!")
        
