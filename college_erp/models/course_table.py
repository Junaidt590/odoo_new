# -*- coding: utf-8 -*-
from odoo import models, fields


class CourseTable(models.Model):
    """course model"""
    _name = "course.table"
    _description = "Course Model"
    _inherit = 'mail.thread'

    name = fields.Char()
    category = fields.Selection(
        selection=[('under graduation', 'Under Graduation'), ('post graduation', 'Post Graduation'),
                   ('diploma', 'Diploma')]
    )
    duration = fields.Integer()
    no_of_semester = fields.Integer()
    sem_ids = fields.One2many('semester.table', 'course_id', required=True)
