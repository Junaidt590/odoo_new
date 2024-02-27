from odoo.http import Controller, request, route


class Admission(Controller):
    """class for student admission through website"""

    @route('/admission', auth='public', website=True)
    def website_admissions(self):
        """function for passing data which is created from website"""
        admission = request.env['admission.table'].search([
            ('website_admission', '=', True)
        ])
        # print(admission)
        return request.render('college_erp.website_admission_details_template',
                              {'admission': admission})

    @route(['''/view/admission/<model("admission.table"):admission>'''], auth='public', website=True)
    def website_admission_details(self, admission):
        """function for passing data to a record """
        print(admission)
        return request.render('college_erp.website_admission_student_template', {'admission': admission})

    @route('/navigate/admission', auth='public', website=True)
    def admission(self):
        """function for passing data to the selection fields of form"""
        course = request.env['course.table'].search([])
        # print(course)
        academic_year = request.env['academic.year'].search([])
        # print(academic_year)
        return request.render('college_erp.website_admission_template',
                              {'course_ids': course, 'academic_year_ids': academic_year})

    @route(route='/create/admission', auth='public', website=True)
    def create_admission(self, **kw):
        """function for creating admission record"""
        print("create admission", kw)
        admission_id = request.env['admission.table'].create({
            'first_name': kw.get('first_name'),
            'last_name': kw.get('last_name'),
            'father': kw.get('father'),
            'mother': kw.get('mother'),
            'communication_address': kw.get('communication_address'),
            'same_as_per_add': kw.get('same_as_per_add'),
            'permanent_address': kw.get('permanent_address'),
            'phone': kw.get('phone'),
            'email': kw.get('email'),
            'course_id': kw.get('course'),
            'academic_year_id': kw.get('academic_year'),
            'website_admission': True
        })
        return request.render('college_erp.website_admission_success_template', 'college_erp.website_admission_details_template', {'admission_id': admission_id})
