{
    'name': "Tax Wise Sales Report",
    'version': '16.0.1.0.0',
    'depends': ['account'],
    'author': "Author Name",
    'category': 'Category',
    'description': """
    Description text
    """,
    # data files always loaded at installation
    'data': [
        'views/tax_report_view.xml',

    ],
    'assets': {
        'web.assets_backend': [
            'tax_wise_sales_report/static/src/components/tax_report.js',
            'tax_wise_sales_report/static/src/components/tax_report.xml',
        ],

    }
}
