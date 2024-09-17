from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    user_id = fields.Many2one('res.users', string='Related User',
                              help='The related user responsible for this employee.')

    @api.model
    def create(self, vals):
        employee = super(HrEmployee, self).create(vals)

        if not employee.user_id:
            user_vals = {
                'name': employee.name,
                'login': vals.get('work_email') or vals.get('private_email'),
                'employee_ids': [(6, 0, [employee.id])],
            }
            user = self.env['res.users'].create(user_vals)


            user.write({'password': 'default_password'})
            user.action_reset_password()

            employee.user_id = user

        return employee
