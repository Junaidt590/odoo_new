import datetime

from odoo import models, api
import io
from odoo.tools.misc import xlsxwriter


class StudentXlsxReport(models.AbstractModel):
    _name = "student.xlsx.report"
    """abstract model model for student wise report xlsx"""

    def get_xlsx_report_values(self, data, response):
        """function for getting report values and printing values to the xlsx"""
        # print(data)
        report_type = data['report_type']
        student_id = data['student_id']
        student = data['student']
        class_name = data['class_name']
        semester_id = data['semester_id']
        exam_id = data['exam_id']
        course_id = data['course_id']
        course = data['course']
        academic_year_id = data['academic_year_id']
        academic_year = data['academic_year']
        exam_type = data['exam_type']
        # print(exam_id)
        if report_type == 'student_wise':
            query = """select admission_table.id, semester_table.id as semester_id, exam_table.id as exam_id,
                                    mark_sheet_table.student_id, mark_sheet_papers.subject, mark_sheet_papers.mark, 
                                    mark_sheet_papers.pass_mark, mark_sheet_papers.result from admission_table
                                    inner join mark_sheet_table on student_id = admission_table.id
                                    inner join course_table on course_table.id = admission_table.course_id
                                    inner join semester_table on semester_table.course_id = course_table.id
                                    inner join exam_table on exam_table.id = mark_sheet_table.exam_id   
                                    inner join mark_sheet_papers on mark_sheet_id = mark_sheet_table.id """
            if not student_id:
                query += """where exam_table.id = '%s' and semester_table.id = '%s'""" % (
                    exam_id, semester_id)
                self.env.cr.execute(query)
                report = self.env.cr.dictfetchall()
                all_students = self.env['admission.table'].search([
                    ('course_id', '=', course_id),
                    ('academic_year_id', '=', academic_year_id)
                ])
                student_data = []
                for student in all_students:
                    student_mark_sheet = self.env['mark.sheet.table'].search([
                        ('student_id', '=', student.id),
                        ('exam_id', '=', exam_id)
                    ])
                    data = {
                        'details': {
                            'student_id': student.id,
                            'name': student.first_name,
                            'course_id': course_id,
                            'course': course,
                            'academic_year_id': academic_year_id,
                            'academic_year': academic_year,
                            'exam_type': exam_type,
                            'result': student_mark_sheet.result if student_mark_sheet else '',
                        }, 'report': [i for i in report if i['student_id'] == student.id]}
                    student_data.append(data)
            else:
                query += """where mark_sheet_table.student_id = '%s' and exam_table.id = '%s' and semester_table.id = '%s'""" % (
                    student_id, exam_id, semester_id)
                print('hai')
                self.env.cr.execute(query)
                report = self.env.cr.dictfetchall()
                student_mark_sheet = self.env['mark.sheet.table'].search([
                    ('student_id', '=', student_id),
                    ('exam_id', '=', exam_id)
                ])
                student_data = []
                data = {
                    'details': {
                        'name': student,
                        'course': course,
                        'academic_year': academic_year,
                        'exam_type': exam_type,
                        'result': student_mark_sheet.result
                    },
                    'report': report}
                student_data.append(data)
            print(student_data)
            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})
            sheet = workbook.add_worksheet()
            cell_format = workbook.add_format(
                {'font_size': '12px', 'align': 'center', 'bold': True})
            cell_format_table = workbook.add_format(
                {'font_size': '12px', 'align': 'center', 'bold': True, 'border': 1})
            head = workbook.add_format(
                {'align': 'center', 'bold': True, 'font_size': '12px', })
            txt = workbook.add_format({'font_size': '12px', 'align': 'center'})
            txt_table = workbook.add_format({'font_size': '12px', 'align': 'center', 'border': 1})
            data_row = 0
            now = str(datetime.datetime.today())
            sheet.write(data_row, 0, now)
            user = self.env.user
            company_name = user.company_id.name
            sheet.write(data_row, 2, company_name)
            data_row += 2
            for data in student_data:
                sheet.write(data_row, 1, 'Student Name:', head)
                sheet.write(data_row, 2, data['details'].get('name'), head)
                data_row += 1
                sheet.write(data_row, 1, data['details'].get('course'), cell_format)
                sheet.write(data_row, 2, data['details'].get('academic_year'), cell_format)
                data_row += 1
                sheet.set_column(data_row, 0, 15)
                sheet.write(data_row, 0, 'Exam Type:', cell_format)
                sheet.write(data_row, 1, data['details'].get('exam_type'), txt)
                data_row += 1
                sheet.write(data_row, 0, 'Result:', cell_format)
                if data['details'].get('result'):
                    sheet.write(data_row, 1, 'Pass', txt)
                else:
                    sheet.write(data_row, 1, 'Failed', txt)
                data_row += 2
                sheet.set_column(data_row, 0, 15)
                sheet.write(data_row, 0, 'Subject', cell_format_table)
                sheet.write(data_row, 1, 'Mark', cell_format_table)
                sheet.write(data_row, 2, 'Pass Mark', cell_format_table)
                sheet.write(data_row, 3, 'Pass/Fail', cell_format_table)

                data_row += 1
                for record in data['report']:
                    sheet.write(data_row, 0, record['subject'], txt_table)
                    sheet.write(data_row, 1, record['mark'], txt_table)
                    sheet.write(data_row, 2, record['pass_mark'], txt_table)
                    if record['result']:
                        sheet.write(data_row, 3, 'Pass', txt_table)
                    else:
                        sheet.write(data_row, 3, 'Failed', txt_table)
                    data_row += 1
                data_row += 4
            workbook.close()
            output.seek(0)
            response.stream.write(output.read())
            output.close()
        elif report_type == 'class_wise':
            class_mark_list = self.env['mark.sheet.table'].search([
                ('exam_id', '=', exam_id)
            ])
            pass_count = class_mark_list.search_count([
                ('exam_id', '=', exam_id),
                ('result', '=', True)
            ])
            fail_count = class_mark_list.search_count([
                ('exam_id', '=', exam_id),
                ('result', '=', False)
            ])
            subjects = self.env['exam.table'].search([
                ('id', '=', exam_id)
            ])
            class_data = {'details': {'class_name': class_name,
                                      'course': course,
                                      'academic_year': academic_year,
                                      'exam_type': exam_type,
                                      'total_students': len(class_mark_list),
                                      'passed_students': pass_count,
                                      'failed_students': fail_count
                                      },
                          'subjects': [],
                          'report': []}
            for record in subjects.papers_ids:
                class_data['subjects'].append({
                    'name': record.subject
                })
            for record in class_mark_list:
                class_data['report'].append({
                    'name': record.student_id.first_name,
                    'marks': [rec.mark for rec in record.papers_ids],
                    'total_marks': record.total_mark,
                    'out_off': record.out_off,
                    'result': record.result
                })
            print(class_data)
            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})
            sheet = workbook.add_worksheet()
            cell_format = workbook.add_format(
                {'font_size': '12px', 'align': 'center', 'bold': True})
            cell_format_table = workbook.add_format(
                {'font_size': '12px', 'align': 'center', 'bold': True, 'border': 1})
            head = workbook.add_format(
                {'align': 'center', 'bold': True, 'font_size': '12px'})
            txt = workbook.add_format({'font_size': '12px', 'align': 'center'})
            txt_table = workbook.add_format({'font_size': '12px', 'align': 'center', 'border': 1})
            # print(data)
            data_row = 0
            sheet.set_column(data_row, 0, 18)
            sheet.set_column(data_row, 1, 18)
            sheet.set_column(data_row, 3, 18)
            now = str(datetime.datetime.today())
            sheet.write(data_row, 0, now)
            user = self.env.user
            company_name = user.company_id.name
            sheet.write(data_row, 2, company_name)
            data_row += 2
            sheet.write(data_row, 1, 'Class Name:', head)
            sheet.set_column(data_row, 2, 23)
            sheet.write(data_row, 2, class_data['details'].get('class_name'), cell_format)
            data_row += 1
            sheet.write(data_row, 1, class_data['details'].get('course'), cell_format)
            sheet.write(data_row, 2, class_data['details'].get('academic_year'), cell_format)
            data_row += 1

            sheet.write(data_row, 0, 'Exam Type:', cell_format)
            sheet.write(data_row, 1, class_data['details'].get('exam_type'), txt)
            data_row += 1
            sheet.write(data_row, 0, 'Total:', cell_format)
            sheet.write(data_row, 1, class_data['details'].get('total_students'), txt)
            data_row += 1
            sheet.write(data_row, 0, 'Pass:', cell_format)
            sheet.write(data_row, 1, class_data['details'].get('passed_students'), txt)
            data_row += 1
            sheet.write(data_row, 0, 'Fail:', cell_format)
            sheet.write(data_row, 1, class_data['details'].get('failed_students'), txt)
            data_row += 2
            sheet.set_column(data_row, 4, 18)
            sheet.write(data_row, 0, 'Student Name', cell_format_table)
            subject_list = [rec.get('name') for rec in class_data['subjects']]
            headings = subject_list + ['Obtained Mark', 'Total Mark', 'Pass/Failed']
            for col, heading in enumerate(headings, 0):
                sheet.write(data_row, col + 1, heading, cell_format_table)
            data_row += 1
            for record in class_data['report']:
                sheet.write(data_row, 0, record.get('name'), txt_table)

                for col, mark in enumerate(record['marks'], 0):
                    sheet.write(data_row, col + 1, mark, txt_table)
                sheet.write(data_row, 3, record['total_marks'], txt_table)
                sheet.write(data_row, 4, record['out_off'], txt_table)
                if record['result']:
                    sheet.write(data_row, 5, 'Pass', txt_table)
                else:
                    sheet.write(data_row, 5, 'Failed', txt_table)
                data_row += 1
            data_row += 4
            workbook.close()
            output.seek(0)
            response.stream.write(output.read())
            output.close()
