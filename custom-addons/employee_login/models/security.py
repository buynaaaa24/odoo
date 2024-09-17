from odoo import models, fields

class SecurityRules(models.Model):
    _name = 'security.rules'

    # Define security-related fields and methods if needed
    name = fields.Char(string='Rule Name')
