# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class ResPartner(models.Model):
    _name = "res.partner"
    _inherit = ['res.partner', 'portal.portal_mixin']

    def _compute_access_url(self):
        super(ResPartner, self)._compute_access_url()
        for partner in self:
            partner.access_url = '/my/identity/%s' % (partner.id)

    def get_access_action(self, access_uid=None):
        self.ensure_one()
        user = access_uid and self.env['res.users'].sudo().browse(access_uid) or self.env.user

        if not user.share and not self.env.context.get('force_website'):
            return super(ResPartner, self).get_access_action(access_uid)
        return {
            'type': 'ir.actions.act_url',
            'url': self.get_portal_url(),
            'target': 'self',
            'res_id': self.id,
        }
