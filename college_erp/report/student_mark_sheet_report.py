# -*- coding: utf-8 -*-
from odoo import models, api


class StudentMarkSheetReport(models.AbstractModel):
    _name = "report.college_erp.student_wise_report_template"
    """abstract model model for student wise report"""

    @api.model
    def _get_report_values(self, docids, data=None):
        """for getting report values"""
        # print(data)
        # print(data.get('report'))
        return {
            'doc_ids': docids,
            'doc_model': 'mark.sheet.report',
            'data': data,
        }


