# Copyright 2015 Oihane Crucelaegui
# Copyright 2015-2019 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html.html

from odoo import api, fields, models


class File(models.Model):
    _inherit = ["multi.company.abstract", "dms.file"]
    _name = "dms.file"

    @api.model
    def create(self, vals):
        vals = self._amend_company_id(vals)
        return super().create(vals)

    @api.model
    def _amend_company_id(self, vals):
        if "company_ids" in vals:
            if not vals["company_ids"]:
                vals["company_id"] = False
            else:
                for item in vals["company_ids"]:
                    if item[0] in (1, 4):
                        vals["company_id"] = item[1]
                    elif item[0] in (2, 3, 5):
                        vals["company_id"] = False
                    elif item[0] == 6:
                        if item[2]:
                            vals["company_id"] = item[2][0]
                        else:  # pragma: no cover
                            vals["company_id"] = False
        elif "company_id" not in vals:
            vals["company_ids"] = False
        return vals
