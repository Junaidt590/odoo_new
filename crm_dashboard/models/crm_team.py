# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields


class CrmTeam(models.Model):
    _inherit = "crm.team"

    crm_stage_id = fields.Many2one('crm.stage', 'Crm Lead Stage')
