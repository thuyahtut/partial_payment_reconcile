# Copyright 2017 Omar Castiñeira, Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountPayment(models.Model):

    _inherit = "account.payment"

    sale_id = fields.Many2one("sale.order", "Sale", readonly=True, states={"draft": [("readonly", False)]})

    def action_open_manual_reconciliation(self):
        print("HELLO")
        return {
            'view_mode': 'form',
            'res_model': 'manual.reconciliation.wizard',
            'type': 'ir.actions.act_window',
            'active_model': 'account.payment',
            'target': 'new',
            'view_id':self.env.ref('partial_payment_reconcile.manual_reconciliation_wizard_form').id,
            'context': {
                'default_partner_id': self.partner_id.id,
                'default_payment_id': self.id,
            }
        }
