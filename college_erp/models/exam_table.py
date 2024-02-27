# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class ExamTable(models.Model):
    """Exam model"""
    _name = "exam.table"
    _description = "Exam Model"
    _inherit = 'mail.thread'

    name = fields.Char(readonly=True, default=lambda self: _('New'), copy=False, compute='compute_exam_name')
    type = fields.Selection(
        selection=[('internal', 'Internal'), ('semester', 'Semester'), ('unit test', 'Unit Test')],
    )
    class_id = fields.Many2one('class.table', required=True)
    semester = fields.Char('Semester', related='class_id.semester_id.name')
    course = fields.Char('Course', related='class_id.semester_id.course_id.name')
    start_date = fields.Date(required=True)
    end_date = fields.Date()
    state = fields.Selection(
        selection=[('draft', 'Draft'), ('confirm', 'Confirm'), ('completed', 'Completed')],
        string='Status', required=True, copy=False,
        tracking=True, default='draft'
    )
    papers_ids = fields.One2many('papers.table', 'exam_id', store=True)
    valuation_count = fields.Integer(compute='compute_count')
    mark_sheet_count = fields.Integer(compute='_mark_sheet_count')

    @api.depends('type', 'class_id')
    def compute_exam_name(self):
        """function for generate exam name"""
        for record in self:
            record.name = f'{record.type} {record.class_id.semester_id.name}'

    @api.model
    def update_state_to_completed(self):
        """function for auto update state to completed when the end date is over"""
        today = fields.Date.today()
        records_to_update = self.search([('end_date', '<=', today), ('state', '!=', 'completed')])
        records_to_update.write({'state': 'completed'})

    def get_valuation(self):
        """function for valuation smart button"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Class',
            'view_mode': 'tree',
            'res_model': 'admission.table',
            'view_id': self.env.ref('college_erp.valuation_tree').id,
            'domain': [('course_id.id', '=', self.class_id.admission_id.course_id.id),
                       ('academic_year_id.id', '=', self.class_id.admission_id.academic_year_id.id),
                       ('id', '=', self.class_id.admission_id.ids)],

            'context': "{'create': False}"
        }

    def compute_count(self):
        """function to display the number count in the smart button valuation"""
        for record in self:
            record.valuation_count = len(self.class_id.admission_id)

    @api.onchange('type')
    def _onchange_is_semester_exam(self):
        """function for when choosing semester auto update subject and max_mark"""
        if self.type == 'semester':
            sem_subject = self.env['syllabus.table'].search([('semester_id', '=', self.class_id.semester_id.id)])
            # print(sem_subject)
            self.papers_ids = [fields.Command.create({
                'subject': sub.subject,
                'max_mark': sub.max_mark
            }) for sub in sem_subject]

    def generate_mark_sheet(self):
        """function for generate mark sheet"""
        students = self.env['admission.table'].search(
            [('id', '=', self.class_id.admission_id.ids)])
        sem_subject = self.papers_ids.search([('exam_id', '=', self.id)])
        for record in students:
            target_record_data = {
                'student_id': record.id,
                'exam_id': self.id,
                'class_id': self.class_id.id,
                'papers_ids': [fields.Command.create({
                    'subject': sub.subject,
                    'max_mark': sub.max_mark,
                    'pass_mark': sub.pass_mark,
                }) for sub in sem_subject]
            }
            self.env['mark.sheet.table'].create(target_record_data)

    def update_mark_sheet(self):
        """function for update mark sheet"""
        mark_sheets_to_update = self.env['mark.sheet.table'].search([
            ('exam_id', '=', self.id),
        ])
        papers = self.papers_ids
        # print(papers)
        for record in mark_sheets_to_update:
            record.papers_ids = [fields.Command.clear()]
            record.papers_ids = [fields.Command.create({
                'subject': sub.subject,
                'max_mark': sub.max_mark,
                'pass_mark': sub.pass_mark,
            }) for sub in papers]

    def _mark_sheet_count(self):
        """function to display the number count in the smart button mark sheet"""
        for record in self:
            record.mark_sheet_count = self.env['mark.sheet.table'].search_count(
                [('exam_id', '=', self.id)])

    def get_mark_sheet(self):
        """function for mark sheet smart button"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Mark Sheet',
            'view_mode': 'tree,form',
            'res_model': 'mark.sheet.table',
            'domain': [('exam_id', '=', self.id)],
            'context': "{'create': False}"
        }
