from odoo import models, Command
from odoo.exceptions import UserError

class EstateAccount(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        self._create_invoices()
        return super().action_sold()

    def _create_invoices(self, grouped=False, final=False, date=None):
        if not self.env['account.move'].check_access_rights('create', False):
            try:
                self.check_access_rights('write')
                self.check_access_rule('write')
            except AccessError:
                return self.env['account.move']

        journal = self.env['account.move'].sudo().with_context(default_move_type='out_invoice')._get_default_journal()
        invoice_vals_list = {
            'partner_id': self.buyer_id, 
            'journal_id': journal.id, 
            'move_type': 'out_invoice',
            "invoice_line_ids": [
                Command.create({
                    "name": '6 percent of the selling price',
                    "quantity": 1,
                    "price_unit": self.best_offer*0.06,
                }),
                Command.create({
                    "name": 'administrative fee',
                    "quantity": 1,
                    "price_unit": 100,
                })
            ]
        }
        return invoice_vals_list
        self.env['account.move'].sudo().with_context(default_move_type='out_invoice').create(invoice_vals_list)
