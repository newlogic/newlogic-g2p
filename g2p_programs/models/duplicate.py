from odoo import fields, models


class G2PDuplicateProgramMembership(models.Model):
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _name = "g2p.program.membership.duplicate"
    _description = "Program Membership duplicate"
    _order = "id desc"

    beneficiary_ids = fields.Many2many("g2p.program_membership", string="Beneficiaries")
    state = fields.Selection(
        selection=[("duplicate", "Duplicate"), ("not_duplicate", "Not Duplicate")]
    )
    deduplication_manager_id = fields.Integer("Deduplication Manager")
    reason = fields.Char("Deduplication Reason")
    comment = fields.Text("Deduplication Comment")
