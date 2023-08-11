from odoo import models, fields


class ComponentProduction(models.Model):
    _name = 'component.production'
    _description = 'Components for production'
    _rec_name = 'name'

    name = fields.Char()
    cost = fields.Float()
    coefficient = fields.Float()
    type = fields.Selection([('wood', 'Wood'), ('epoxy_resin', 'Epoxy Resin')], default='wood')
