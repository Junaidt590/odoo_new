# -*- coding: utf-8 -*-
{
    'name': 'CRM Dashboard',
    'version': '16.0.1.0.0',
    'sequence': -100,
    'depends': ['crm', 'sales_team'],
    'author': "Aswin Ak",
    'category': 'crm',
    'assets': {
        'web.assets_backend': [
            'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.js',
            # 'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.8.0/Chart.bundle.js',
            # 'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.4/Chart.js',
            'crm_dashboard/static/src/js/client_action.js',
            'crm_dashboard/static/src/xml/clent_action_template.xml',
        ],
    },
    'data': [
        'views/client_action.xml',
        'views/crm_team.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
