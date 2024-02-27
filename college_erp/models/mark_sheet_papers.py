# -*- coding: utf-8 -*-
from odoo import models, fields, api


class MarkSheetPapers(models.Model):
    """Mark sheet papers model"""
    _name = "mark.sheet.papers"
    _description = "Mark Sheet Papers Model"

    subject = fields.Char(store=True, readonly=True)
    mark = fields.Float()
    max_mark = fields.Float(store=True, readonly=True)
    pass_mark = fields.Float(store=True, readonly=True)
    result = fields.Boolean('Pass/Fail', store=True, compute='compute_result')
    mark_sheet_id = fields.Many2one('mark.sheet.table', 'Mark sheet')

    @api.depends('pass_mark', 'mark')
    def compute_result(self):
        """function for auto change result"""
        for record in self:
            if record.mark >= record.pass_mark:
                record.result = True
            else:
                record.result = False
