# Part of Newlogic G2P. See LICENSE file for full copyright and licensing details.
import logging

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class G2PMultiEntitlementApprovalWiz(models.TransientModel):
    _name = "g2p.multi.entitlement.approval.wizard"
    _description = "Multi Entitlement Approval Wizard"

    @api.model
    def default_get(self, fields):
        res = super(G2PMultiEntitlementApprovalWiz, self).default_get(fields)
        _logger.info(
            "Adding to Multi Entitlement Approval Wizard with IDs: %s"
            % self.env.context.get("active_ids")
        )
        if self.env.context.get("active_ids"):
            entitlement_ids = []
            cycle_id = 0
            for rec in self.env.context.get("active_ids"):
                entitlement = self.env["g2p.entitlement"].search(
                    [
                        ("id", "=", rec),
                    ]
                )
                if entitlement.state in ("draft", "pending_validation"):
                    entitlement_ids.append([0, 0, {"entitlement_id": rec}])

                cycle_id = entitlement.cycle_id.id

            cycle = self.env["g2p.cycle"].search(
                [
                    ("id", "=", cycle_id),
                ]
            )
            if cycle:
                if cycle.state == "approved":
                    res["cycle_id"] = cycle_id
                else:
                    raise ValidationError(
                        _("You can approve only entitlements from approved cycles.")
                    )
            res["entitlement_ids"] = entitlement_ids

        return res

    entitlement_ids = fields.One2many(
        "g2p.multi.entitlement.approval",
        "wizard_id",
        string="Entitlements",
        required=True,
    )
    cycle_id = fields.Many2one(
        "g2p.cycle",
        "Cycle",
        help="A Cycle",
    )

    def approve_entitlements(self):
        for rec in self.entitlement_ids:

            if rec.entitlement_id.state in ("draft", "pending_validation"):
                # Prepare journal entry (account.move) via account.payment
                payment = {
                    "partner_id": rec.entitlement_id.partner_id.id,
                    "payment_type": "outbound",
                    "amount": rec.entitlement_id.initial_amount,
                    "currency_id": rec.entitlement_id.journal_id.currency_id.id,
                    "journal_id": rec.entitlement_id.journal_id.id,
                    "partner_type": "supplier",
                }
                new_payment = self.env["account.payment"].create(payment)
                rec.entitlement_id.update(
                    {
                        "disbursement_id": new_payment.id,
                        "state": "approved",
                        "date_approved": fields.Date.today(),
                    }
                )

    def open_wizard(self):

        _logger.info("Entitlement IDs: %s" % self.env.context.get("active_ids"))
        return {
            "name": "Multiple Entitlements Approval",
            "view_mode": "form",
            "res_model": "g2p.multi.entitlement.approval.wizard",
            "view_id": self.env.ref(
                "g2p_programs.multi_entitlement_approval_wizard_form_view"
            ).id,
            "type": "ir.actions.act_window",
            "target": "new",
            "context": self.env.context,
        }


class G2PMultiEntitlementApproval(models.TransientModel):
    _name = "g2p.multi.entitlement.approval"
    _description = "Multi Entitlement Approval"

    entitlement_id = fields.Many2one(
        "g2p.entitlement",
        "Entitlement",
        help="A Entitlement",
        required=True,
    )
    wizard_id = fields.Many2one(
        "g2p.multi.entitlement.approval.wizard",
        "Multi Entitlement Approval Wizard",
        help="A Wizard",
        required=True,
    )
    cycle_id = fields.Many2one(
        "g2p.cycle",
        "Cycle",
        help="A Cycle",
    )
    state = fields.Selection(
        [
            ("New", "New"),
            ("Okay", "Okay"),
            ("Conflict", "Conflict"),
            ("Approved", "Approved"),
        ],
        "Status",
        readonly=True,
        default="New",
    )
