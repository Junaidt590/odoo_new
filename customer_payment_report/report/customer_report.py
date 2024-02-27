# -*- coding: utf-8 -*-
from odoo import models, api
from odoo.exceptions import ValidationError


class CustomerReport(models.AbstractModel):
    """ Abstract model"""
    _name = 'report.customer_payment_report.report_customer_payment'
    _description = 'Customer Payment report Abstract model'

    @api.model
    def _get_report_values(self, docids, data=None):
        """to return data to be displayed in the report"""
        print(data)
        # print(docids)
        
        # query = """
        #         select a.name,a.invoice_date,a.invoice_partner_display_name,sum(l.price_subtotal),
        #         sum(l.cgst),sum(l.igst),a.amount_total
        #         from account_move as a
        #         left join account_move_line as l on a.id=l.move_id
        #         """
        # term = 'Where '
        # if data['from_date']:
        #     query += "where a.invoice_date >= '%s'" % data['from_date']
        #     term = ' AND '
        # if data['to_date']:
        #     query += term + "a.invoice_date <= '%s' " % data['to_date']
        #     term = ' AND '
        # query += term + "tax_audit like 'BASE%' group by a.name,a.invoice_date,a.invoice_partner_display_name," \
        #                 "a.amount_total order by a.name"
        # self._cr.execute(query)
        # docs = self._cr.fetchall()
        # if not docs:
        #     raise ValidationError("No record to print!!!")
        # val = {
        #     'doc_ids': docids,
        #     'doc_model': 'sale.report.wizard',
        #     'docs': docs,
        #     'data': data,
        # }
        # return val
