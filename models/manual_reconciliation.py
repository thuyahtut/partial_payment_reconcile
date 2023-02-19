from odoo import _, api, fields, models
from odoo.exceptions import UserError

class ManualReconciliationLines(models.Model):
    _name = 'manual.reconciliation.line'
    _description = 'Manual Reconciliation Lines'

    name = fields.Char('Description')
    invoice_id = fields.Many2one('account.move', string='Invoices')
    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True, default=lambda self: self.env.company.currency_id)
    amount_residual = fields.Monetary(string="Amount Due", store=True, currency_field='currency_id', related='invoice_id.amount_residual')
    pay_amount = fields.Monetary(string="Payment", store=True, currency_field='currency_id')
    manual_reconciliation_id = fields.Many2one('manual.reconciliation.wizard', string='Reconciliation', ondelete='cascade')
    
class ManualReconciliation(models.Model):
    _name = 'manual.reconciliation.wizard'
    _description = 'Manual Reconciliation'

    payment_id = fields.Many2one('account.payment', string='Payment')
    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True, related='payment_id.currency_id')
    av_amount = fields.Monetary(string="Amount", store=True, currency_field='currency_id', related='payment_id.amount')
    partner_id = fields.Many2one('res.partner', string='Partner')
    invoice_ids = fields.Many2many('account.move', string='Invoices')
    line_ids = fields.One2many('manual.reconciliation.line', 'manual_reconciliation_id', string='Matching')

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        if self.partner_id:
            values = []
            partner_inv_ids = self.env['account.move'].search([('partner_id', '=', self.partner_id.id), ('move_type', '=', 'out_invoice'), ('amount_residual', '>', 0), ('payment_state', 'not in', ['in_payment', 'paid'])])
            for inv in partner_inv_ids:
                values.append((0, 0, {'invoice_id': inv.id}))
            self.update({'line_ids': values})           


    def confirm_action(self):
        balance_receiv = self.payment_id.move_id.line_ids.filtered(lambda l: l.account_id.internal_type == 'receivable')
        for line in self.line_ids:
            invoice = self.env['account.move'].browse(line.invoice_id.id)
            invoice.custom_assign_outstanding_line(balance_receiv.id,line.pay_amount)

