# Copyright 2017 Omar Castiñeira, Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api, _


class AccountPayment(models.Model):

    _inherit = "account.payment"

    sale_id = fields.Many2one("sale.order", "Sale", readonly=True, states={"draft": [("readonly", False)]})

    manual_rec_ids = fields.One2many('manual.reconciliation.wizard', 'payment_id', string='Manual Reconciliation')

    manual_reconciled_count = fields.Integer('Reconcile', compute='_compute_manual_rec_ids')

    @api.depends('manual_rec_ids')
    def _compute_manual_rec_ids(self):
        for record in self:
            record.manual_reconciled_count = len(record.manual_rec_ids)

    # def button_open_manual_rec(self):
    #     return {
    #             'view_mode': 'form',
    #             'res_model': 'manual.reconciliation.wizard',
    #             'type': 'ir.actions.act_window',
    #             'domain': [('id', 'in', self.manual_rec_ids.ids)],
    #             # 'active_model': 'account.payment',
    #             # 'target': 'new',
    #             # 'view_id':self.env.ref('partial_payment_reconcile.manual_reconciliation_wizard_form').id,
    #             # 'context': {
    #             #     'default_partner_id': self.partner_id.id,
    #             #     'default_payment_id': self.id,
    #             # }
    #         }

    def button_open_manual_rec(self):
        ''' Redirect the user to the invoice(s) paid by this payment.
        :return:    An action on account.move.
        '''
        self.ensure_one()

        action = {
            'name': _("Manual Reconciliation"),
            'type': 'ir.actions.act_window',
            'res_model': 'manual.reconciliation.wizard',
            'context': {'create': False},
        }
        if len(self.manual_rec_ids) == 1:
            action.update({
                'view_mode': 'form',
                'res_id': self.manual_rec_ids.id,
            })
        else:
            action.update({
                'view_mode': 'list,form',
                'domain': [('id', 'in', self.manual_rec_ids.ids)],
            })
        return action


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
