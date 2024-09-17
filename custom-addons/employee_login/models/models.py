# models.py
from odoo import models, fields

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    custom_field = fields.Char(string='Custom Field')
