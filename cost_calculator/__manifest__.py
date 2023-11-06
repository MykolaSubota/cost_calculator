{
    'name': 'Price Calculator',
    'author': 'Mykola Subota',
    'version': '0.2.11',
    'summary': 'Calculator for calculating the cost of tables.',
    'sequence': 100,
    'category': 'Inventory/Inventory',
    'depends': ['base', 'account'],
    'data': [
        'views/component_production_view.xml',
        'views/record_calculator_view.xml',
        'views/parameter_calculator_view.xml',
        'data/parameter_data.xml',
        'views/menu_view.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
