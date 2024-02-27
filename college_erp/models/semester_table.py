# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SemesterTable(models.Model):
    """semester model"""
    _name = "semester.table"
    _description = "Semester Table"
    _inherit = 'mail.thread'

    name = fields.Char(compute='_compute_name', readonly=True, store=True)
    no_of_semester = fields.Integer()
    course_id = fields.Many2one('course.table', string='Course', required=True)
    syllabus_ids = fields.One2many('syllabus.table', 'semester_id')

    @api.depends('no_of_semester', 'course_id')
    def _compute_name(self):
        """function for generate semester name"""
        for record in self:
            record.name = str(record.no_of_semester) + " " + "Sem: " + str(record.course_id.name)
