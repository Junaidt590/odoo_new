# -*- coding: utf-8 -*-
from odoo import models, fields


class PromotionTable(models.Model):
    """Promotion model"""
    _name = "promotion.table"
    _description = "Promotion Model"
    _rec_name = "exam_id"

    exam_id = fields.Many2one('exam.table', 'Exam')
    exam_class = fields.Char('Class', related='exam_id.class_id.name')
    semester = fields.Char('Semester', related='exam_id.class_id.semester_id.name')
    promoted_students_ids = fields.One2many('mark.sheet.table', 'promotion_id')
    state = fields.Selection(
        selection=[('pending', 'Pending'), ('completed', 'Completed')],
        default='pending'
    )
    hide_generate_button = fields.Boolean(default=False)
    hide_promote_button = fields.Boolean(default=False)

    def generate_promotion(self):
        promoted_students_ids = self.env['mark.sheet.table'].search([
            ('class_id.id', '=', self.exam_id.class_id.id),
            ('exam_id.id', '=', self.exam_id.id),
        ])
        self.promoted_students_ids = promoted_students_ids.filtered(lambda l: l.result is True)
        self.hide_generate_button = True
        if self.hide_generate_button:
            self.hide_promote_button = True

    def promote_students(self):
        promote_class = self.exam_id.class_id.promotion_class_id
        # print(promote_class)
        students = self.promoted_students_ids.search([
            ('promotion_id', '=', self.id)
        ])
        pass_students = students.student_id
        # print(pass_students)
        pass_students.write({'class_id': promote_class})
        self.write({
            'state': "completed"
        })
        self.hide_promote_button = False
        
