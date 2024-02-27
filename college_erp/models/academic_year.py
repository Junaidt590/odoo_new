# -*- coding: utf-8 -*-
from odoo import models, fields


class AcademicYear(models.Model):
    """academic year model"""
    _name = "academic.year"
    _description = "Academic Model"

    name = fields.Char()
