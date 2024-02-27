# -*- coding: utf-8 -*-
from odoo import models, fields


class PapersTable(models.Model):
    """Papers model"""
    _name = "papers.table"
    _description = "Papers Model"

    subject = fields.Char(store=True)
    max_mark = fields.Integer(store=True)
    pass_mark = fields.Integer(store=True)
    exam_id = fields.Many2one('exam.table', 'Exam')
