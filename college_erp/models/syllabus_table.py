# -*- coding: utf-8 -*-
from odoo import models, fields


class SyllabusTable(models.Model):
    """Syllabus model"""
    _name = "syllabus.table"
    _description = "Syllabus Model"

    subject = fields.Char()
    max_mark = fields.Integer()
    semester_id = fields.Many2one('semester.table', 'Semester', required=True)
    exam_id = fields.Many2one('exam.table', 'Exam')
