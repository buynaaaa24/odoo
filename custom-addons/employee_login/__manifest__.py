{
    'name': 'Real Estate Ads Employee Login',
    'version': '1.0',
    'summary': 'Module for employee login and dashboard',
    'description': 'Provides a custom login as employee and dashboard functionality.',
    'author': 'Your Name',
    'website': 'http://www.example.com',
    'category': 'Human Resources',
    'depends': ['base', 'hr', 'project'],
    'data': [
        'security/security.xml',  # Security rules and access control
        'views/employee_view.xml',  # Employee form view customization
        'views/employee_dashboard_template.xml',  # Dashboard template
        'views/employee_login_template.xml',
        'views/menu_items.xml',
        'views/employee_login_view.xml',
    ],
    "installable": True,
    "application": True,
    "license": "GPL-3",
}
