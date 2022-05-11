#
# Copyright (c) 2022 Newlogic.
#
# This file is part of newlogic-g2p-erp.
# See https://github.com/newlogic/newlogic-g2p-erp/ for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from odoo import fields, models

from ..components.odk_client import ODKClient


class ImportSourceODK(models.Model):
    """Import source for JSON files on ODK."""

    _name = "import.source.odk"
    _inherit = "import.source"
    _description = "JSON import source through ODK"
    _source_type = "json_odk"
    _reporter_model = "reporter.csv"

    #
    # json_file = fields.Binary("JSON file")
    # # use these to load file from an FS path
    # json_filename = fields.Char("CSV filename")

    # overide the default
    # chunk_size = fields.Integer(required=True, default=100, string="Chunks Size")

    # Overrided to get a store field for env purpose
    name = fields.Char(compute=False)
    odata_url = fields.Char(
        string="OData URL", required=True
    )  # https://odk.newlogic-demo.com/v1/projects/1/forms/idpass_ona_registration_example.svc
    email = fields.Char("Email", required=True)
    password = fields.Char("Password", required=True)

    source_id = fields.Many2one("g2p.datasource", "Source")
    tags = fields.Many2many("g2p.additional.data.tags", string="Tags")
    location_id = fields.Many2one("g2p.location", "Location")

    # TODO: Do we need company_id?

    # @property
    # def _config_summary_fields(self):
    #     _fields = super()._config_summary_fields
    #     _fields.extend(
    #         [
    #             "odata_url",
    #             "email",
    #         ]
    #     )
    #     return _fields

    def _inject_config(self, results):
        """Inject config to data."""
        source_id = None
        location_id = None
        tag_ids = []

        # force external IDs
        # self.export_data(['source_id', 'location_id', 'tags'])

        if self.source_id:
            self.source_id.export_data(["id"])
            source_id = list(self.source_id.get_external_id().values())[0]
        if self.location_id:
            self.location_id.export_data(["id"])
            location_id = list(self.location_id.get_external_id().values())[0]

        for result in results["value"]:
            result["source_id"] = source_id
            result["location_id"] = location_id
            result["tag_ids"] = tag_ids

    def get_lines(self):
        """Retrieve lines to import."""
        self.ensure_one()

        odk_client = ODKClient(self.odata_url, self.email, self.password)

        # retrieve results
        skip = 0
        results = self._get_page(odk_client, skip)
        self._inject_config(results)
        yield results["value"]
        while results.get("@odata.nextLink", None) is not None:
            skip += len(results["values"])
            results = self._get_page(odk_client, skip)
            self._inject_config(results)
            yield results["value"]

    def _get_page(self, odk_client, skip):
        results = odk_client.get_responses(skip, self.chunk_size)
        return results
