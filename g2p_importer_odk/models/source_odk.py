import base64
import os
import json

from ..components.odk_client import ODKClient
from odoo import fields, models


class ImportSourceODK(models.Model):
    """Import source for JSON files on ODK."""

    _name = "import.source.json.odk"
    _inherit = "import.source"
    _description = "JSON import source through ODK"
    _source_type = "json_odk"
    _reporter_model = "reporter.csv"

    odk_client = None
    #
    # json_file = fields.Binary("JSON file")
    # # use these to load file from an FS path
    # json_filename = fields.Char("CSV filename")

    # overide the default
    chunk_size = fields.Integer(required=True, default=100, string="Chunks Size")

    # Overrided to get a store field for env purpose
    name = fields.Char(compute=False)
    odata_url = fields.Char(string="OData URL", required=True) # https://odk.newlogic-demo.com/v1/projects/1/forms/idpass_ona_registration_example.svc
    email = fields.Char('Email', required=True)
    password = fields.Char('Password', required=True)

    source_id = fields.Many2one('g2p.datasource', 'Source')
    tags = fields.Many2many('g2p.additional.data.tags', string='Tags')
    location_id = fields.Many2one('g2p.location', 'Location')

    # TODO: Do we need company_id?

    @property
    def _config_summary_fields(self):
        _fields = super()._config_summary_fields
        _fields.extend(
            [
                "odata_url",
                "email",
            ]
        )
        return _fields

    def get_lines(self):
        """Retrieve lines to import."""
        self.ensure_one()

        if self.odk_client is None:
            self.odk_client = ODKClient(self.odata_url, self.email, self.password)

        # retrieve results
        skip = 0
        results = self._get_page(skip)
        yield results['values']
        while results.get('@odata.nextLink', None) is not None:
            skip += len(results['values'])
            results = self._get_page(skip)
            yield results['values']

    def _get_page(self, skip):
        results = self.odk_client.get_responses(skip, self.chunk_size)
        return results
