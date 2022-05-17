# Copyright 2022 CreuBlanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class DmsFile(models.Model):
    _inherit = "dms.file"

    def action_execute_action(self):
        self.ensure_one()
        action = self.env.ref("dms_action.dms_action_file_act_window").read()[0]
        action["context"] = {"default_dms_file_id": self.id}
        return action
