from odoo import models, fields


class ParameterCalculator(models.Model):
    _name = 'parameter.calculator'
    _description = 'Parameters'
    _rec_name = 'name'

    name = fields.Char(translate=True)
    code = fields.Char()
    value = fields.Float()
