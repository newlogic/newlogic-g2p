from odoo import api, models


class ImportSourceConsumerMixin(models.AbstractModel):
    _inherit = "import.source.consumer.mixin"

    @api.model
    def _selection_source_ref_id(self):
        selection = super()._selection_source_ref_id()
        new_source = ("import.source.json.ODK", "JSON ODK")
        if new_source not in selection:
            selection.append(new_source)
        return selection
