from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def action_reset_password(self):

        res = super(ResUsers, self).action_reset_password()

        user = self
        if user.password:
            self._check_password_strength(user.password)
        return res

    def _check_password_strength(self, password):

        min_length = 6
        if len(password) < min_length:
            raise ValidationError(f'Password must be at least {min_length} characters long.')


