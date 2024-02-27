# -*- coding: utf-8 -*-
from odoo import models, api


class AccountMoveLine(models.Model):
    """inherited account move line model """
    _inherit = 'account.move.line'

    @api.model
    def get_action_print_report(self):
        """function for generating report"""
        from_date = self.env.context.get('from_date')
        to_date = self.env.context.get('to_date')
        # print(from_date)
        # print(to_date)
        indian_taxes = self.env['account.tax'].search([
            ('country_id.name', '=', 'India'),
            ('amount_type', '=', 'group')
        ])
        ret_list = []
        for i in indian_taxes:
            print(i.name)
            data = {
                'tax_id': i.id,
                'tax_name': i.name,
                'report': []
            }
            records = self.env['account.move'].search([
                # ('tax_ids', '=', i.id)
                ('sequence_prefix', '=', 'INV/2023/'),
                ('line_ids.tax_ids', '=', i.id),
                ('invoice_date', '>=', from_date) if from_date else (),
                ('invoice_date', '<=', to_date) if to_date else (),
            ])
            print(records)
            for record in records:
                # print(record.name)
                tax_records = self.search([
                    ('move_name', '=', record.name)
                ])
                # print(tax_records)
                product_line = tax_records.filtered(lambda l: l.product_id)
                filtered_product_line = product_line.filtered(lambda l: l.tax_ids.id == i.id)
                # print(filtered_product_line)
                inv_taxable_value = sum(filtered_product_line.mapped('price_unit'))
                # print(inv_taxable_value)
                tax_invoice_sgst = 0
                tax_invoice_cgst = 0
                tax_invoice_igst = 0
                sgst = []
                cgst = []
                igst = []
                filtered_tax = tax_records.filtered(lambda l: l.display_type == 'tax')
                for line in filtered_product_line:
                    filtered_tax_line = filtered_tax.filtered(lambda l: l.group_tax_id == line.tax_ids)
                    # print(filtered_tax_line)
                    tax_invoice_sgst = filtered_tax_line.filtered(lambda l: l.name == 'sgst').credit
                    # print(tax_invoice_sgst)
                    tax_invoice_cgst = filtered_tax_line.filtered(lambda l: l.name == 'cgst').credit
                    tax_invoice_igst = filtered_tax_line.filtered(lambda l: l.name == 'igst').credit
                sgst.append(tax_invoice_sgst)
                cgst.append(tax_invoice_cgst)
                igst.append(tax_invoice_igst)
                # print(sum(sgst), sum(cgst), sum(igst))
                total_sgst = sum(sgst)
                total_cgst = sum(cgst)
                total_igst = sum(igst)
                data['report'].append({
                    'id': record.id,
                    'invoice': record.name,
                    'taxable': inv_taxable_value,
                    'sgst': total_sgst,
                    'cgst': total_cgst,
                    'igst': total_igst,
                    'net_amount': (
                                total_sgst + total_cgst + total_igst + inv_taxable_value)
                })

            ret_list.append(data)
        print(ret_list)
        return ret_list



