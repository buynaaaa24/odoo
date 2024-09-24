from odoo import http
from odoo.http import request


class EmployeeLoginController(http.Controller):

    @http.route('/employee_login', type='http', auth='public', website=True)
    def employee_login(self, **kw):
        # Render the employee login form
        return request.render('your_module.employee_login_template', {})

    @http.route('/employee_login/authenticate', type='http', auth='public', website=True, methods=['POST'])
    def employee_authenticate(self, **kw):
        login = kw.get('login')  # Get the email login
        password = kw.get('password')

        # Find the employee record by email (login)
        employee = request.env['hr.employee'].search([('work_email', '=', login)], limit=1)  # Adjust field as necessary

        if employee and request.session.authenticate(request.session.db, login, password):
            return request.redirect('/employee_dashboard')
        else:
            return request.redirect('/employee_login?error=1')

    @http.route('/employee_dashboard', type='http', auth='user', website=True)
    def employee_dashboard(self, **kw):
        user = request.env.user
        if not user or not user.has_group('your_module.group_employee'):
            return request.redirect('/web/login')

        tasks = request.env['project.task'].search([('user_id', '=', user.id)])
        companies = request.env['res.company'].search([])

        return request.render('your_module.employee_dashboard_template', {
            'tasks': tasks,
            'companies': companies,
        })
