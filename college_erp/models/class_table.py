# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class ClassTable(models.Model):
    """class model"""
    _name = "class.table"
    _description = "Class Table"
    _inherit = 'mail.thread'

    name = fields.Char(compute='_compute_class_name', default=lambda self: _('New'), readonly=True, store=True)
    semester_id = fields.Many2one('semester.table', 'Semester', store=True)
    course = fields.Char('Course', required=True, related='semester_id.course_id.name')
    academic_year_id = fields.Many2one('academic.year', string='Academic Year', required=True)
    admission_id = fields.One2many('admission.table', 'class_id')
    promotion_class_id = fields.Many2one('class.table','Promotion Class')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Class name already exists !"),
    ]

    @api.depends('semester_id', 'academic_year_id')
    def _compute_class_name(self):
        """function for compute class name"""
        for record in self:
            record.name = f'{record.semester_id.name} {record.academic_year_id.name}'

    @api.onchange('academic_year_id')
    def change_student_list(self):
        """function for compute students list in the class"""
        for record in self:
            record.admission_id = self.env['admission.table'].search([
                ('academic_year_id.id', '=', record.academic_year_id.id),
                ('course_id.id', '=', record.semester_id.course_id.id),
                ('course_id.sem_ids.id', '=', record.semester_id.id),
                ('state', '!=', 'rejected'),
                ('class_id', '=', False)

            ])


