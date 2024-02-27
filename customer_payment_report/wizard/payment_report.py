from odoo import models, fields
from odoo.exceptions import ValidationError


class CustomerPaymentReport(models.TransientModel):
    _name = 'payment.report'
    _description = 'Payment Report'

    date_from = fields.Date(string='From')
    date_to = fields.Date(string='To')

    def action_print_report(self):
        """print button action"""
        # if self.date_from < self.date_to:
        #     raise ValidationError("The from date should be earlier tha ending date")
        # for move in self:
        #     record = self.env['account.move.line'].search([('move_id', '=', int(move.id))])[1].tax_ids
        #     print(record)
        data = {
            'from_date': self.date_from,
            'to_date': self.date_to,
        }
        return self.env.ref('customer_payment_report.action_payment_report').report_action(self, data=data)
