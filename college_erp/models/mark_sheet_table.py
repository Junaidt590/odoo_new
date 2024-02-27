# -*- coding: utf-8 -*-
from odoo import models, fields, api


class MarkSheetTable(models.Model):
    """Mark sheet model"""
    _name = "mark.sheet.table"
    _description = "Mark Sheet Model"
    _rec_name = 'student_id'

    student_id = fields.Many2one('admission.table', 'Student', domain="[('class_id', '=', class_id)]", store=True)
    exam_id = fields.Many2one('exam.table', 'Exam', required=True)
    class_id = fields.Many2one('class.table', 'Class')
    course = fields.Char('Course', required=True, related='class_id.semester_id.course_id.name')
    semester = fields.Char('Semester', required=True, related='class_id.semester_id.name')
    result = fields.Boolean('Pass/Fail', compute='compute_result_button', store=True)
    rank = fields.Float()
    papers_ids = fields.One2many('mark.sheet.papers', 'mark_sheet_id')
    total_mark = fields.Float("Total", compute='compute_total_mark', store=True)
    out_off = fields.Float("Out Off", compute='compute_total_mark', store=True)
    promotion_id = fields.Many2one('promotion.table')

    _sql_constraints = [
        ('name_uniq', 'unique (student_id.name)', "Mark sheet already exists !"),
    ]

    @api.onchange('student_id')
    def change_papers(self):
        """function for auto update subject, max_mark, pass_mark"""
        for record in self:
            if record.exam_id:
                sem_subject = self.env['papers.table'].search([('exam_id', '=', self.exam_id.id)])
                # print(sem_subject)
                self.papers_ids = [fields.Command.create({
                    'subject': sub.subject,
                    'max_mark': sub.max_mark,
                    'pass_mark': sub.pass_mark,
                }) for sub in sem_subject]

    @api.depends('papers_ids.result')
    def compute_result_button(self):
        """Compute the pass or failed students in exam.It checks the pass or fail
        by each subject and shows whether the student passed the exam.
        if any of the subject fails the student mark as failed. """
        for rec in self:
            is_pass = True
            for record in rec.papers_ids:
                if not record.result:
                    is_pass = False
            if is_pass:
                rec.result = True
            else:
                rec.result = False

    @api.depends('papers_ids.mark', 'papers_ids.max_mark')
    def compute_total_mark(self):
        """function for calculate total mark"""
        for record in self:
            total_mark = sum(record.papers_ids.mapped('mark'))
            out_off = sum(record.papers_ids.mapped('max_mark'))
            record.total_mark = total_mark
            record.out_off = out_off
