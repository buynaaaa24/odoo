# controllers/main.py
from odoo import http
from odoo.http import request


class EmployeeLoginController(http.Controller):

    @http.route('/employee_login', type='http', auth='user')
    def employee_login(self, **kw):
        user = request.env.user
        if not user or not user.has_group('your_module.group_employee'):
            return request.redirect('/web/login')

        return request.redirect('/web')

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
