{
    'name': "Customer Payment Report",
    'version': '16.0.1.0.0',
    'depends': ['account'],
    'author': "Author Name",
    'category': 'Inventory',

    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'wizard/payment_report_form.xml',
        'report/report.xml',
        'report/payment_report_template.xml',
        'views/payment_report_view.xml',
    ],
    'installable': True,
    'auto_install': True,
}