import math

from odoo import models, fields, api


class RecordCalculator(models.Model):
    _name = 'record.calculator'
    _rec_name = 'client'
    _description = 'Calculator records'

    client = fields.Many2one('res.partner')
    length = fields.Float('Length (in mm)', required=True)
    width = fields.Float('Width (in mm)', required=True)
    thickness = fields.Float('Thickness (in mm)', required=True)
    wood = fields.Many2one('component.production', domain=[('type', '=', 'wood')])
    epoxy_resin = fields.Many2one('component.production', domain=[('type', '=', 'epoxy_resin')])
    form = fields.Selection([('oval', 'Oval'), ('rectangle', 'Rectangle')], default='rectangle')
    tinting = fields.Boolean()
    living_land = fields.Boolean('Living edge')
    burned_edge = fields.Boolean()
    waterfall = fields.Selection(
        [('0', 'Missing'), ('1', 'One side'), ('2', 'Two sides')],
        default='0',
        required=True
    )
    polishing = fields.Boolean()
    warning = fields.Char(readonly=True, compute='_compute_warning')
    square = fields.Float('Square (in m2)', (12, 5), readonly=True, compute='_compute_square')
    perimeter = fields.Float('Perimeter (in m)', (12, 5), readonly=True, compute='_compute_perimeter')
    volume = fields.Float('Volume (in m3)', (12, 5), readonly=True, compute='_compute_volume')
    fill_volume = (
        fields.Float('Fill volume (in m3)', (12, 5), readonly=True, compute='_compute_epoxy_resin'))
    cost_of_epoxy_resin = fields.Float(
        'Cost of epoxy resin (in USD)',
        (12, 5),
        readonly=True,
        compute='_compute_cost_of_epoxy_resin')
    cost_of_wood = (
        fields.Float('Cost of wood (in USD)', (12, 5), readonly=True, compute='_compute_cost_of_wood'))
    additional_expenses = fields.Float(
        'Additional expenses (in USD)',
        (12, 5),
        readonly=True,
        compute='_compute_additional_expenses'
    )
    wood_preparation_time = fields.Float(
        'Wood preparation time (in minutes)',
        (12, 5),
        readonly=True,
        compute='_compute_wood_preparation_time'
    )
    formwork_assembly_time = fields.Float(
        'Formwork assembly time (in minutes)',
        (12, 5),
        readonly=True,
        compute='_compute_formwork_assembly_time'
    )
    filling_time = (
        fields.Float('Filling time (in minutes)', (12, 5), readonly=True, compute='_compute_filling_time'))
    cnc_installation_time = (
        fields.Float('CNC installation time (in minutes)', (12, 5), readonly=True))
    alignment_time_on_cnc = fields.Float(
        'Alignment time on CNC (in minutes)',
        (12, 5),
        readonly=True,
        compute='_compute_alignment_time_on_cnc'
    )
    cutting_time_along_contour = fields.Float(
        'Cutting time along contour (in minutes)',
        (12, 5),
        readonly=True,
        compute='_compute_cutting_time_along_contour'
    )
    slot_milling_time = fields.Float('Slot milling time (in minutes)', (12, 5), readonly=True)
    calibration_time = fields.Float(
        'Calibration time (in minutes)',
        (12, 5),
        readonly=True,
        compute='_compute_calibration_time'
    )
    grinding_time = fields.Float(
        'Grinding time (in minutes)',
        (12, 5),
        readonly=True,
        compute='_compute_grinding_time'
    )
    edge_grinding_time = fields.Float(
        'Edge grinding time (in minutes)',
        (12, 5),
        readonly=True,
        compute='_compute_edge_grinding_time'
    )
    time_for_living_land = fields.Float(
        'Time for "living land" (in minutes)',
        (12, 5),
        readonly=True,
        compute='_compute_time_for_living_land'
    )
    edge_burning_time = fields.Float(
        'Edge burning time (in minutes)',
        (12, 5),
        readonly=True,
        compute='_compute_edge_burning_time'
    )
    polishing_time = fields.Float(
        'Polishing time (in minutes)',
        (12, 5),
        readonly=True,
        compute='_compute_polishing_time'
    )
    time_of_coverage = fields.Float(
        'Time of coverage (in minutes)',
        (12, 5),
        readonly=True,
        compute='_compute_time_of_coverage'
    )
    time_of_assembly = fields.Float('Time of assembly (in minutes)', (12, 5), readonly=True)
    packing_time = (
        fields.Float('Packing time (in minutes)', (12, 5), readonly=True, compute='_compute_packing_time'))
    total_amount_of_working_time = fields.Float(
        'Total amount of working time (in hours)',
        (12, 5),
        readonly=True,
        compute='_compute_total_amount_of_working_time'
    )
    cost_of_work = (
        fields.Float('Cost of work (in USD)', (12, 5), readonly=True, compute='_compute_cost_of_work'))
    coefficients = fields.Char(readonly=True, compute='_compute_coefficients')
    total_ratio = fields.Float(readonly=True, compute='_compute_total_ratio')
    total_cost = fields.Float('Total cost (in USD)', (12, 5), readonly=True, compute='_compute_total_cost_')
    total_cost_uah = (
        fields.Float('Total cost (in UAH)', (12, 5), readonly=True, compute='_compute_total_cost_uah'))
    percentage_of_filling = fields.Selection(
        [('MNM', 'Minimum'), ('AVR', 'Average'), ('MXM', 'Maximum')],
        default='AVR'
    )

    @api.depends('width', 'thickness')
    def _compute_warning(self):
        for rec in self:
            if rec.width > 1250 and rec.thickness > 55:
                rec.warning = 'Attention: If the width and thickness of the worktop are too large, individual ' \
                              'approval is required!'
            elif rec.width > 1250:
                rec.warning = 'Attention: The width of the worktop is too wide, individual approval is required!'
            elif rec.thickness > 55:
                rec.warning = 'Attention: If the thickness of the worktop is too large, individual approval is ' \
                              'required!'
            else:
                rec.warning = ''

    @api.depends('width', 'length', 'form')
    def _compute_square(self):
        for rec in self:
            if rec.form == 'oval':
                rec.square = round(3.1415 / 4 * rec.length * rec.width / 1000000, 5)
            else:
                rec.square = round(rec.length * rec.width / 1000000, 5)

    @api.depends('width', 'length', 'form')
    def _compute_perimeter(self):
        for rec in self:
            if rec.form == 'oval':
                rec.perimeter = round(2 * 3.1415 * math.sqrt((rec.length ** 2 + rec.width ** 2) / 8) / 1000, 5)
            else:
                rec.perimeter = round((rec.length + rec.width) * 2 / 1000, 5)

    @api.depends('width', 'length', 'thickness')
    def _compute_volume(self):
        for rec in self:
            rec.volume = round(rec.length * rec.width / 1000000 * rec.thickness / 1000 * 1.5, 5)

    @api.depends('epoxy_resin', 'volume', 'polishing', 'percentage_of_filling')
    def _compute_epoxy_resin(self):
        for rec in self:
            if rec.epoxy_resin:
                rec.fill_volume = \
                    round(
                        rec.volume *
                        self.env['parameter.calculator'].search([('code', '=', rec.percentage_of_filling)]).value / 100
                        / 1.5 * 1000 * (1.2 if rec.polishing else 1),
                        5
                    )
            else:
                rec.fill_volume = 0

    @api.depends('fill_volume')
    def _compute_cost_of_epoxy_resin(self):
        epoxy_resin_delivery_cost = self.env['parameter.calculator'].search([('code', '=', 'EPX')]).value
        for rec in self:
            if rec.epoxy_resin:
                rec.cost_of_epoxy_resin = round(
                    rec.fill_volume / 1000 * (rec.epoxy_resin.cost + epoxy_resin_delivery_cost) * 1000,
                    5
                )
            else:
                rec.cost_of_epoxy_resin = 0

    @api.depends('fill_volume', 'wood')
    def _compute_cost_of_wood(self):
        cost_of_wood_delivery = self.env['parameter.calculator'].search([('code', '=', 'CST')]).value
        for rec in self:
            rec.cost_of_wood = \
                (rec.wood.cost + cost_of_wood_delivery) * (rec.volume - rec.fill_volume / 1000) * rec.wood.coefficient

    @api.depends('square')
    def _compute_additional_expenses(self):
        additional_expenses = self.env['parameter.calculator'].search([('code', '=', 'ADD')]).value
        for rec in self:
            rec.additional_expenses = round(additional_expenses * rec.square, 5)

    @api.depends('square')
    def _compute_wood_preparation_time(self):
        wood_preparation_time = self.env['parameter.calculator'].search([('code', '=', 'WDP')]).value
        for rec in self:
            rec.wood_preparation_time = wood_preparation_time * rec.square

    @api.depends('square')
    def _compute_formwork_assembly_time(self):
        formwork_assembly_time = self.env['parameter.calculator'].search([('code', '=', 'FRM')]).value
        for rec in self:
            rec.formwork_assembly_time = formwork_assembly_time * rec.square

    @api.depends('fill_volume')
    def _compute_filling_time(self):
        filling_time = self.env['parameter.calculator'].search([('code', '=', 'FLL')]).value
        for rec in self:
            rec.filling_time = filling_time * math.ceil(rec.fill_volume / 18)

    @api.depends('square')
    def _compute_alignment_time_on_cnc(self):
        cnc_installation_time = self.env['parameter.calculator'].search([('code', '=', 'CNC')]).value
        alignment_time_on_cnc = self.env['parameter.calculator'].search([('code', '=', 'ALG')]).value
        for rec in self:
            rec.cnc_installation_time = cnc_installation_time
            rec.alignment_time_on_cnc = alignment_time_on_cnc * rec.square

    @api.depends('perimeter', 'thickness')
    def _compute_cutting_time_along_contour(self):
        cutting_time_along_contour = self.env['parameter.calculator'].search([('code', '=', 'CTT')]).value
        for rec in self:
            rec.cutting_time_along_contour = cutting_time_along_contour * rec.perimeter * rec.thickness

    @api.depends('square')
    def _compute_calibration_time(self):
        slot_milling_time = self.env['parameter.calculator'].search([('code', '=', 'SLT')]).value
        calibration_time = self.env['parameter.calculator'].search([('code', '=', 'CLB')]).value
        for rec in self:
            rec.slot_milling_time = slot_milling_time
            rec.calibration_time = calibration_time * rec.square

    @api.depends('square')
    def _compute_grinding_time(self):
        grinding_time = self.env['parameter.calculator'].search([('code', '=', 'GRN')]).value
        for rec in self:
            rec.grinding_time = grinding_time * rec.square

    @api.depends('perimeter')
    def _compute_edge_grinding_time(self):
        edge_grinding_time = self.env['parameter.calculator'].search([('code', '=', 'EDG')]).value
        for rec in self:
            rec.edge_grinding_time = edge_grinding_time * rec.perimeter

    @api.depends('length', 'living_land')
    def _compute_time_for_living_land(self):
        time_for_living_land = self.env['parameter.calculator'].search([('code', '=', 'TMF')]).value
        for rec in self:
            if rec.living_land:
                rec.time_for_living_land = time_for_living_land * rec.length * 2 / 1000
            else:
                rec.time_for_living_land = 0

    @api.depends('length', 'burned_edge')
    def _compute_edge_burning_time(self):
        edge_burning_time = self.env['parameter.calculator'].search([('code', '=', 'EDB')]).value
        for rec in self:
            if rec.burned_edge:
                rec.edge_burning_time = edge_burning_time * rec.length * 2 / 1000
            else:
                rec.edge_burning_time = 0

    @api.depends('square')
    def _compute_polishing_time(self):
        polishing_time = self.env['parameter.calculator'].search([('code', '=', 'PLS')]).value
        for rec in self:
            if rec.polishing:
                rec.polishing_time = polishing_time * rec.square
            else:
                rec.polishing_time = 0

    @api.depends('square')
    def _compute_time_of_coverage(self):
        time_of_coverage = self.env['parameter.calculator'].search([('code', '=', 'TMC')]).value
        for rec in self:
            rec.time_of_coverage = time_of_coverage * rec.square

    @api.depends('square')
    def _compute_packing_time(self):
        time_of_assembly = self.env['parameter.calculator'].search([('code', '=', 'TMS')]).value
        packing_time = self.env['parameter.calculator'].search([('code', '=', 'PCK')]).value
        for rec in self:
            rec.time_of_assembly = time_of_assembly
            rec.packing_time = packing_time * rec.square

    @api.depends(
        'wood_preparation_time',
        'formwork_assembly_time',
        'filling_time',
        'cnc_installation_time',
        'alignment_time_on_cnc',
        'cutting_time_along_contour',
        'slot_milling_time',
        'calibration_time',
        'grinding_time',
        'edge_grinding_time',
        'time_for_living_land',
        'edge_burning_time',
        'polishing_time',
        'time_of_coverage',
        'time_of_assembly',
        'packing_time',
        'waterfall'
    )
    def _compute_total_amount_of_working_time(self):
        for rec in self:
            waterfall_time = 0
            if rec.waterfall == '1':
                waterfall_time = self.env["parameter.calculator"].search([("code", "=", "TMW")]).value
            elif rec.waterfall == '2':
                waterfall_time = self.env["parameter.calculator"].search([("code", "=", "TMW")]).value * 2
            rec.total_amount_of_working_time = round(
                (rec.wood_preparation_time + rec.formwork_assembly_time + rec.filling_time + rec.cnc_installation_time +
                 rec.alignment_time_on_cnc + rec.cutting_time_along_contour + rec.slot_milling_time +
                 rec.calibration_time + rec.grinding_time + rec.edge_grinding_time + rec.time_for_living_land +
                 rec.polishing_time + rec.time_of_coverage + rec.time_of_assembly + rec.packing_time + rec.burned_edge +
                 waterfall_time) / 60,
                5
            )

    @api.depends('total_amount_of_working_time')
    def _compute_cost_of_work(self):
        labour_costs = self.env['parameter.calculator'].search([('code', '=', 'LBR')]).value
        for rec in self:
            rec.cost_of_work = round(rec.total_amount_of_working_time * labour_costs, 5)

    @api.depends('epoxy_resin', 'tinting', 'living_land', 'polishing', 'burned_edge', 'waterfall')
    def _compute_coefficients(self):
        for rec in self:
            coefficients = str(self.env['parameter.calculator'].search([('code', '=', 'INT')]).value)
            if rec.epoxy_resin:
                coefficients += f'; {rec.epoxy_resin.coefficient}'
            if rec.tinting:
                coefficients += f'; {self.env["parameter.calculator"].search([("code", "=", "TNT")]).value}'
            if rec.living_land:
                coefficients += f'; {self.env["parameter.calculator"].search([("code", "=", "CFF")]).value}'
            if rec.burned_edge:
                coefficients += f'; {self.env["parameter.calculator"].search([("code", "=", "EDR")]).value}'
            if rec.polishing:
                coefficients += f'; {self.env["parameter.calculator"].search([("code", "=", "PLH")]).value}'
            if rec.waterfall != '0':
                coefficients += f'; {self.env["parameter.calculator"].search([("code", "=", "WTR")]).value if rec.waterfall == "1" else self.env["parameter.calculator"].search([("code", "=", "WTR")]).value * 2}'
            rec.coefficients = coefficients

    @api.depends('coefficients')
    def _compute_total_ratio(self):
        for rec in self:
            total_ratio = self.env['parameter.calculator'].search([('code', '=', 'INT')]).value
            if rec.epoxy_resin:
                total_ratio *= rec.epoxy_resin.coefficient
            if rec.tinting:
                total_ratio *= self.env["parameter.calculator"].search([("code", "=", "TNT")]).value
            if rec.living_land:
                total_ratio *= self.env["parameter.calculator"].search([("code", "=", "CFF")]).value
            if rec.burned_edge:
                total_ratio *= self.env["parameter.calculator"].search([("code", "=", "EDR")]).value
            if rec.polishing:
                total_ratio *= self.env["parameter.calculator"].search([("code", "=", "PLH")]).value
            if rec.waterfall != '0':
                total_ratio *= (
                    self.env["parameter.calculator"].search([("code", "=", "WTR")]).value) if rec.waterfall == '1' \
                    else self.env["parameter.calculator"].search([("code", "=", "WTR")]).value * 2
            rec.total_ratio = round(total_ratio, 5)

    @api.depends(
        'cost_of_wood',
        'cost_of_epoxy_resin',
        'cost_of_work',
        'total_ratio',
        'additional_expenses',
        'wood'
    )
    def _compute_total_cost_(self):
        for rec in self:
            if not rec.wood:
                rec.total_cost = 0
                return
            rec.total_cost = round(
                (rec.cost_of_wood + rec.cost_of_epoxy_resin + rec.cost_of_work) * rec.total_ratio +
                rec.additional_expenses,
                5
            )

    @api.depends('total_cost')
    def _compute_total_cost_uah(self):
        for rec in self:
            rec.total_cost_uah = (
                    rec.total_cost / self.env['res.currency'].search([('name', '=', 'USD')], limit=1).rate)
