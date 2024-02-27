# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class AdmissionTable(models.Model):
    """admission model"""
    _name = "admission.table"
    _description = "Admission Model"
    _rec_name = 'first_name'
    _inherit = 'mail.thread'

    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    father = fields.Char()
    mother = fields.Char()
    communication_address = fields.Char(required=True)
    same_as_per_add = fields.Boolean(string='Same as permanent address')
    permanent_address = fields.Char()
    phone = fields.Char('Phone')
    email = fields.Char(required=True)
    course_id = fields.Many2one('course.table', string='Course')
    date_of_application = fields.Date(default=fields.Datetime.now())
    academic_year_id = fields.Many2one('academic.year', string='Academic Year')
    previous_education = fields.Selection(
        selection=[('higher secondary', 'Higher Secondary'), ('ug', 'UG'), ('pg', 'PG')]
    )
    educational_institute = fields.Char()
    transfer_certificate = fields.Binary(string='Upload TC')
    state = fields.Selection(
        selection=[('draft', 'Draft'), ('application', 'Application'), ('approved', 'Approved'), ('done', 'Done'),
                   ('rejected', 'Rejected')],
        string='Status', required=True, copy=False,
        tracking=True, default='draft'
    )
    joining_date = fields.Date(compute="_compute_joining_date")
    student_ids = fields.One2many('student.table', 'admission_id')
    class_id = fields.Many2one('class.table', 'Class')
    website_admission = fields.Boolean(default=False)

    _sql_constraints = [
        ('email_uniq', 'unique(email)', "Email already exists !"),
    ]

    @api.depends("date_of_application")
    def _compute_joining_date(self):
        """function for get joining date"""
        now = fields.Datetime.now()
        for record in self:
            record.joining_date = record.date_of_application = now + timedelta(days=10)

    def button_confirm(self):
        """function for confirm button"""
        self.write({
            'state': "application"
        })
        for rec in self:
            if rec.transfer_certificate == 0:
                raise ValidationError(_("Upload your TC"))

    def button_reject(self):
        """function for reject button"""
        self.write({
            'state': "rejected"
        })
        mail_template = self.env.ref('college_erp.mail_template_reject_admission')
        mail_template.send_mail(self.id, force_send=True)

    def create_student(self):
        """function for auto student creation during admission"""
        for source_record in self:
            target_record_data = {
                'first_name': source_record.first_name,
                'last_name': source_record.last_name,
                'father': source_record.father,
                'mother': source_record.mother,
                'communication_address': source_record.communication_address,
                'same_as_per_add': source_record.same_as_per_add,
                'permanent_address': source_record.permanent_address,
                'phone': source_record.phone,
                'email': source_record.email,
                'admission_id': source_record.id,
            }
            self.env['student.table'].create(target_record_data)
            self.write({
                'state': "done"
            })
        mail_template = self.env.ref('college_erp.mail_template_confirm_admission')
        mail_template.send_mail(self.id, force_send=True)
