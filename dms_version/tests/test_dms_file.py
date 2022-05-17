# Copyright 2017-2020 MuK IT GmbH
# Copyright 2021 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64

from odoo.addons.dms.tests.common import DocumentsBaseCase, multi_users


class TestFileVersion(DocumentsBaseCase):
    def _setup_test_data(self):
        super()._setup_test_data()
        self.storage_demo = self.env.ref("dms.storage_demo")
        self.storage_demo.sudo().write({"has_versioning": True})

    @multi_users(lambda self: self.multi_users(), callback="_setup_test_data")
    def test_file_version(self):
        dms_file = self.env.ref("dms.file_13_demo")
        self.assertFalse(dms_file.current_revision_id)
        self.assertTrue(dms_file.active)
        dms_file.write({"content": base64.b64encode(b"\xff new")})
        self.assertTrue(dms_file.current_revision_id)
        self.assertFalse(dms_file.active)
        self.assertTrue(dms_file.current_revision_id.active)
        self.assertEqual(dms_file.current_revision_id.revision_number, 1)
        self.assertIn(dms_file, dms_file.current_revision_id.old_revision_ids)
        self.assertEqual(dms_file.current_revision_id.revision_count, 1)
