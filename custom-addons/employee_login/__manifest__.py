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
        'data/data.xml',  # Initial data or demo data if needed
    ],
    'installable': True,
    'application': True,
}
