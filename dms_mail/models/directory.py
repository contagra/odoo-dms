# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, models


class DmsDirectory(models.Model):
    _inherit = "dms.directory"

    def _filter_dms_directory(self, user):
        def _filter(dms_directory):
            if dms_directory.storage_id.filter_by_message_partner_ids:
                Model = self.env[dms_directory.res_model]
                if hasattr(Model, 'message_partner_ids'):
                    model = Model.search([('id', '=', dms_directory.res_id), ('message_partner_ids', 'child_of', [user.commercial_partner_id.id])])
                    return len(model) > 0
                return False
            return True
        return _filter

    @api.depends("child_directory_ids")
    def _compute_count_directories(self):
        for record in self:
            filtered_directories = record.child_directory_ids.filtered(self._filter_dms_directory(self.env.user))
            directories = len(filtered_directories)
            record.count_directories = directories
            record.count_directories_title = _("%s Subdirectories") % directories
