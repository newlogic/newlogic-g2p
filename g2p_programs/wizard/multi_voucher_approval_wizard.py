# Part of Newlogic G2P. See LICENSE file for full copyright and licensing details.
import logging

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class G2PMultiVoucherApprovalWiz(models.TransientModel):
    _name = "g2p.multi.voucher.approval.wizard"
    _description = "Multi Voucher Approval Wizard"

    @api.model
    def default_get(self, fields):
        res = super(G2PMultiVoucherApprovalWiz, self).default_get(fields)
        _logger.info(
            "Adding to Multi Voucher Approval Wizard with IDs: %s"
            % self.env.context.get("active_ids")
        )
        if self.env.context.get("active_ids"):
            voucher_ids = []
            cycle_id = 0
            for rec in self.env.context.get("active_ids"):
                voucher = self.env["g2p.voucher"].search(
                    [
                        ("id", "=", rec),
                    ]
                )
                if voucher.state in ("draft", "pending_validation"):
                    voucher_ids.append([0, 0, {"voucher_id": rec}])

                cycle_id = voucher.cycle_id.id

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
                        _(
                            "Only approved Cycle are allowed to multiple voucher approval"
                        )
                    )
            res["voucher_ids"] = voucher_ids

        return res

    voucher_ids = fields.One2many(
        "g2p.multi.voucher.approval",
        "wizard_id",
        string="Vouchers",
        required=True,
    )
    cycle_id = fields.Many2one(
        "g2p.cycle",
        "Cycle",
        help="A Cycle",
    )

    def approve_vouchers(self):
        for rec in self.voucher_ids:

            if rec.voucher_id.state in ("draft", "pending_validation"):
                # Prepare journal entry (account.move) via account.payment
                payment = {
                    "partner_id": rec.voucher_id.partner_id.id,
                    "payment_type": "outbound",
                    "amount": rec.voucher_id.initial_amount,
                    "currency_id": rec.voucher_id.journal_id.currency_id.id,
                    "journal_id": rec.voucher_id.journal_id.id,
                    "partner_type": "supplier",
                }
                new_payment = self.env["account.payment"].create(payment)
                rec.voucher_id.update(
                    {
                        "disbursement_id": new_payment.id,
                        "state": "approved",
                        "date_approved": fields.Date.today(),
                    }
                )

    def open_wizard(self):

        _logger.info("Voucher IDs: %s" % self.env.context.get("active_ids"))
        return {
            "name": "Multiple Vouchers Approval",
            "view_mode": "form",
            "res_model": "g2p.multi.voucher.approval.wizard",
            "view_id": self.env.ref(
                "g2p_programs.multi_voucher_approval_wizard_form_view"
            ).id,
            "type": "ir.actions.act_window",
            "target": "new",
            "context": self.env.context,
        }


class G2PMultiVoucherApproval(models.TransientModel):
    _name = "g2p.multi.voucher.approval"
    _description = "Multi Voucher Approval"

    voucher_id = fields.Many2one(
        "g2p.voucher",
        "Voucher",
        help="A Voucher",
        required=True,
    )
    wizard_id = fields.Many2one(
        "g2p.multi.voucher.approval.wizard",
        "Multi Voucher Approval Wizard",
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
