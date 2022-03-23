# Copyright 2017-2020 MuK IT GmbH
# Copyright 2021 Tecnativa - Víctor Martínez
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class DmsFile(models.Model):
    _name = "dms.file"
    _inherit = ["dms.file", "base.revision"]

    current_revision_id = fields.Many2one(
        comodel_name="dms.file",
    )
    old_revision_ids = fields.One2many(
        comodel_name="dms.file",
    )
    # TODO: Move to base_revision addon
    revisions_count = fields.Integer(compute="_compute_revisions_count")

    @api.depends("old_revision_ids")
    def _compute_revisions_count(self):
        res = (
            self.with_context(active_test=False)
            .read_group(
                domain=[("current_revision_id", "in", self.ids)],
                fields=["current_revision_id"],
                groupby=["current_revision_id"],
            )
        )
        revision_dict = {
            x["current_revision_id"][0]: x["current_revision_id_count"] for x in res
        }
        for rec in self:
            rec.revisions_count = revision_dict.get(rec.id, 0)

    def action_view_revision(self):
        self.ensure_one()
        action = self.env.ref("dms_version.action_dms_revisions_file")
        return action.read()[0]
