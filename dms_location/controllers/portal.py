# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import http
from odoo.http import request

from odoo.addons.dms.controllers.portal import CustomerPortal
from odoo.addons.web.controllers.main import ensure_db


class ResPartnerCustomerPortal(CustomerPortal):

    @http.route(
        ["/my/identity/<int:partner_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_dms_location(self, partner_id=False, access_token=None, **kw):
        ensure_db()
        res = self._dms_check_access("res.partner", partner_id, access_token)
        if not res:
            if access_token:
                return request.redirect("/")
            else:
                return request.redirect("/my")
        res_partner_sudo = res
        # values
        values = {
            "page_name": "dms_location",
            "default_url": "/my/identity",
            "access_token": access_token,
            "res_partner": res_partner_sudo,
        }
        return request.render("dms_location.portal_my_identity", values)
