# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class DmsStorage(models.Model):
    _inherit = "dms.storage"

    filter_by_message_partner_ids = fields.Boolean(
        default=False,
        help="Indicates if directories are only visible to followers.",
    )
