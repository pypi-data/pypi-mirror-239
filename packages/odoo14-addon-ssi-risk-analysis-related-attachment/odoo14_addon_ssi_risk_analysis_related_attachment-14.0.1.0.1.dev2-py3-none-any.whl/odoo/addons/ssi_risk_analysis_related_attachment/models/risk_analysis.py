# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class RiskAnalysis(models.Model):
    _name = "risk_analysis"
    _inherit = [
        "risk_analysis",
        "mixin.related_attachment",
    ]
    _related_attachment_create_page = True
