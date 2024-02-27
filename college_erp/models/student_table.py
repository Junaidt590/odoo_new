# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class StudentTable(models.Model):
    """student model"""
    _name = "student.table"
    _description = "College Model"
    _inherit = 'mail.thread'
    _rec_name = 'first_name'

    admission_no = (fields.Char(string="Admission No",
                                readonly=True, default=lambda self: _('New'), copy=False))
    admission_date = fields.Date(default=fields.Datetime.now())
    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    father = fields.Char()
    mother = fields.Char()
    communication_address = fields.Char()
    same_as_per_add = fields.Boolean(string='Same as permanent address')
    permanent_address = fields.Char()
    phone = fields.Char('Phone')
    email = fields.Char(required=True)
    admission_id = fields.Many2one('admission.table', 'admission')

    @api.model
    def create(self, vals):
        """sequence generation of admission number"""
        # print(vals)
        if vals.get('admission_no', _('New')) == _('New'):
            # print(vals)
            vals['admission_no'] = self.env['ir.sequence'].next_by_code(
                'student.table') or _('New')
        res = super(StudentTable, self).create(vals)
        return res
