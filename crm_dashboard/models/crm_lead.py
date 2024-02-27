# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, models
import datetime
# import seaborn as sns


class CrmTeam(models.Model):
    _inherit = "crm.lead"

    @api.model
    def get_dashboard_details(self, filter_value):
        current_date = datetime.date.today()
        domain = []
        if filter_value == 'This year':
            first_day_of_year = datetime.date(current_date.year, 1, 1)
            last_day_of_year = datetime.date(current_date.year, 12, 31)
            domain = [('create_date', '>', first_day_of_year), ('create_date', '<', last_day_of_year)]
        elif filter_value == 'This quarter':
            quarter = (current_date.month - 1) // 3 + 1
            print(current_date.month)
            first_day_of_quarter = datetime.date(current_date.year,
                                                 3 * quarter - 2, 1)
            # Calculate the last day of the quarter
            if quarter == 4:
                last_day_of_quarter = datetime.date(current_date.year, 12, 31)
            else:
                last_day_of_quarter = datetime.date(
                    current_date.year, 3 * quarter + 1, 1
                ) - datetime.timedelta(days=1)
            domain = [('create_date', '>', first_day_of_quarter),
                      ('create_date', '<', last_day_of_quarter)]

        elif filter_value == 'This month':
            first_day_of_month = datetime.date(current_date.year,
                                               current_date.month, 1)
            # Calculate the last day of the month
            if current_date.month == 12:
                last_day_of_month = datetime.date(current_date.year,
                                                  current_date.month, 31)
            else:
                last_day_of_month = datetime.date(current_date.year,
                                                  current_date.month + 1,
                                                  1) - datetime.timedelta(
                    days=1)

            domain = [('create_date', '>', first_day_of_month),
                      ('create_date', '<', last_day_of_month)]
        elif filter_value == 'This week':
            first_day_of_week = current_date - datetime.timedelta(
                days=current_date.weekday())
            # Determine the last day of the week (Saturday)
            last_day_of_week = first_day_of_week + datetime.timedelta(days=6)
            domain = [('create_date', '>', first_day_of_week),
                      ('create_date', '<', last_day_of_week)]
        all_leads = self.search(domain)
        user = self.env.user
        invoices = self.env['account.move'].search([])
        if user.has_group('sales_team.group_sale_manager'):
            print("admin.....")
            return {
                'myleads': len(all_leads.filtered(
                lambda l: l.type == 'lead')),
                'lead_ids': all_leads.filtered(
                    lambda l: l.type == 'lead').ids,
                'myopportunity': len(all_leads.filtered(
                    lambda l: l.type == 'opportunity')),
                'opportunity_ids': all_leads.filtered(
                    lambda l: l.type == 'opportunity').ids,
                'expected_revenue': round(
                    sum(all_leads.mapped('expected_revenue')), 2),
                'currency': self.env.user.company_id.currency_id.symbol,
                'revenue': round(sum(invoices.mapped('amount_total')), 2),
                'win_ratio': sum(all_leads.mapped('probability')) / len(
                    all_leads) if len(all_leads) != 0 else 0
            }
        invoiced_amt = sum(
            invoices.filtered(lambda l: l.user_id.id == user.id).mapped(
                'amount_total'))
        return_vals = {
            'myleads': len(all_leads.filtered(
            lambda l: l.user_id.id == user.id and l.type == 'lead')),
            'lead_ids': all_leads.filtered(
                lambda l: l.user_id.id == user.id and l.type == 'lead').ids,
            'myopportunity': len(all_leads.filtered(
                lambda l: l.user_id.id == user.id and l.type == 'opportunity')),
            'opportunity_ids': all_leads.filtered(
                lambda l: l.user_id.id == user.id and l.type == 'opportunity'
            ).ids,
            'expected_revenue': round(
                sum(all_leads.mapped('expected_revenue')), 2),
            'currency': self.env.user.company_id.currency_id.symbol,
            'revenue': round(invoiced_amt, 2),
            'win_ratio': sum(all_leads.mapped('probability')) / len(
                all_leads) if len(all_leads) != 0 else 0
        }
        return return_vals

    @api.model
    def get_lead_lost_graph_data(self):
        print('get_lead_lost_graph_data')
        search_data = self.search([('lost_reason_id', '!=', False), ('active', 'in', [False, True])])

        # for data in search_data:
        #     if data.lost_reason_id:
        #         print("hi")
        #     else:
        #         print("k")
        # print(search_data)
        # print(search_data.filtered(lambda l: l.lost_reason_id is not False))
        # print(self.search([])[0].lost_reason_id)
        lost_ids = [lead.lost_reason_id for lead in search_data]
        occurrence_dict = {}
        for lost_id in lost_ids:
            if lost_id in occurrence_dict:
                continue
            occurrence_dict[lost_id] = lost_ids.count(lost_id)
        labels = []
        data = []
        color_names = ["red", "green", "blue", "yellow", "purple", "orange",
                       "pink", "black", "white", "brown"]
        for key, value in occurrence_dict.items():
            labels.append(key.name)
            data.append(value)
        graph_data = {
            'labels': labels,
            'datasets': [{
                'barPercentage': 0.5,
                'minBarLength': 2,
                'categoryPercentage': 0.8,
                # 'yAxisID': 'Lost Lead Count',
                'backgroundColor': color_names[:len(data)],
                'data': data
            }]
        }
        return graph_data

    @api.model
    def get_pie_chart_data(self):
        activities = self.search([]).activity_ids
        activity_type_ids = [activity.activity_type_id for activity in activities]
        occurrence_dict = {}
        for type_id in activity_type_ids:
            if type_id in occurrence_dict:
                continue
            occurrence_dict[type_id] = activity_type_ids.count(type_id)

        data = []
        labels = []
        for key, val in occurrence_dict.items():
            data.append(val)
            labels.append(key.name)
        color_names = ["red", "green", "blue", "yellow", "black", "white",
                       "brown", "purple", "orange", "pink"]
        return {
                'labels': labels,
                'datasets': [{
                    'label': 'My First Dataset',
                    'backgroundColor': color_names[-len(data):],
                    'hoverOffset': 8,
                    'data': data
                }]
            }

    @api.model
    def get_lead_table_data(self):
        current_date = datetime.date.today()
        first_day_of_month = datetime.date(
            current_date.year, current_date.month, 1)
        leads = self.search_read([('type', '=', 'lead'),
                             ('create_date', '>=', first_day_of_month),
                             ('create_date', '<=', current_date)])

        print(leads,first_day_of_month,current_date)
        return leads




