# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, http
from odoo.http import request
from odoo.osv.expression import OR

from odoo.addons.dms.controllers.portal import CustomerPortal
from odoo.addons.web.controllers.main import ensure_db


class DmsMailCustomerPortal(CustomerPortal):

    def _filter_dms_directory(self, user):

        def _filter(dms_directory):
            if dms_directory.storage_id.filter_by_message_partner_ids:
                Model = request.env[dms_directory.res_model]
                if hasattr(Model, 'message_partner_ids'):
                    model = Model.search(
                        [
                            ('id', '=', dms_directory.res_id),
                            (
                                'message_partner_ids', 'child_of',
                                [user.commercial_partner_id.id]
                            )
                        ]
                    )
                    return len(model) > 0
                return False
            return True

        return _filter

    @http.route(
        ["/my/dms/directory/<int:dms_directory_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_dms_directory(
        self,
        dms_directory_id=False,
        sortby=None,
        filterby=None,
        search=None,
        search_in="name",
        access_token=None,
        **kw
    ):
        ensure_db()
        # operations
        searchbar_sortings = {"name": {"label": _("Name"), "order": "name asc"}}
        # default sortby br
        if not sortby:
            sortby = "name"
        sort_br = searchbar_sortings[sortby]["order"]
        # search
        searchbar_inputs = {
            "name": {"input": "name", "label": _("Name")},
        }
        if not filterby:
            filterby = "name"
        # domain
        domain = [
            ("is_hidden", "=", False), ("parent_id", "=", dms_directory_id)
        ]
        # search
        if search and search_in:
            search_domain = []
            if search_in == "name":
                search_domain = OR([search_domain, [("name", "ilike", search)]])
            domain += search_domain
        # content according to pager and archive selected
        if access_token:
            dms_directory_items = (
                request.env["dms.directory"].sudo().search(
                    domain, order=sort_br
                )
            )
        else:
            dms_directory_items = request.env["dms.directory"].search(
                domain, order=sort_br
            )
        dms_directory_items = dms_directory_items.filtered(
            self._filter_dms_directory(request.env.user)
        )
        request.session["my_dms_folder_history"] = dms_directory_items.ids
        res = self._dms_check_access(
            "dms.directory", dms_directory_id, access_token
        )
        if not res:
            if access_token:
                return request.redirect("/")
            else:
                return request.redirect("/my")
        dms_directory_sudo = res
        # dms_files_count
        domain = [
            ("is_hidden", "=", False),
            ("directory_id", "=", dms_directory_id),
        ]
        # search
        if search and search_in:
            search_domain = []
            if search_in == "name":
                search_domain = OR([search_domain, [("name", "ilike", search)]])
            domain += search_domain
        # items
        if access_token:
            dms_file_items = (
                request.env["dms.file"].sudo().search(domain, order=sort_br)
            )
        else:
            dms_file_items = request.env["dms.file"].search(
                domain, order=sort_br
            )
        request.session["my_dms_file_history"] = dms_file_items.ids
        dms_parent_categories = dms_directory_sudo.sudo(
        )._get_parent_categories(access_token)
        # values
        values = {
            "dms_directories": dms_directory_items,
            "page_name": "dms_directory",
            "default_url": "/my/dms",
            "searchbar_sortings": searchbar_sortings,
            "searchbar_inputs": searchbar_inputs,
            "search_in": search_in,
            "sortby": sortby,
            "filterby": filterby,
            "access_token": access_token,
            "dms_directory": dms_directory_sudo,
            "dms_files": dms_file_items,
            "dms_parent_categories": dms_parent_categories,
        }
        return request.render("dms.portal_my_dms", values)