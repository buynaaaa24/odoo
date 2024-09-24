from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    user_id = fields.Many2one('res.users', string='Related User',
                               help='The related user responsible for this employee.')

    @api.model
    def create(self, vals):
        # Create the employee record
        employee = super(HrEmployee, self).create(vals)

        # Check if there's no related user
        if not employee.user_id:
            user_vals = {
                'name': employee.name,
                'login': vals.get('work_email') or vals.get('private_email'),
                'employee_ids': [(6, 0, [employee.id])],
                'groups_id': [(6, 0, [self.env.ref('your_module.employee_group_id').id])],  # Optional: Assign user group
            }
            user = self.env['res.users'].create(user_vals)

            # Optionally set a default password or send a reset link
            user.action_reset_password()

            # Assign the created user to the employee
            employee.user_id = user

        return employee
