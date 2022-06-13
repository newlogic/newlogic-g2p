# Part of Newlogic G2P. See LICENSE file for full copyright and licensing details.
import logging

from odoo import _, api, fields, models

# from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class G2PCreateNewProgramWiz(models.TransientModel):
    _name = "g2p.program.create.wizard"
    _description = "Create a New Program Wizard"

    @api.model
    def default_get(self, fields):
        _logger.info("Creating a new program")
        res = super(G2PCreateNewProgramWiz, self).default_get(fields)

        # Set default currency from the user's current company
        currency_id = (
            self.env.user.company_id.currency_id
            and self.env.user.company_id.currency_id.id
            or None
        )
        res["currency_id"] = currency_id
        return res

    name = fields.Char("Program Name", required=True)
    currency_id = fields.Many2one("res.currency", "Currency", required=True)

    # Eligibility Manager
    eligibility_domain = fields.Text(string="Domain", default="[]", required=True)

    # Cycle Manager
    auto_approve_entitlements = fields.Boolean(
        string="Auto-approve Entitlements", default=False
    )
    cycle_duration = fields.Integer("Cycle Duration", default=30, required=True)
    approver_group_id = fields.Many2one(
        comodel_name="res.groups",
        string="Approver Group",
    )

    # Entitlement Manager
    amount_per_cycle = fields.Monetary(
        currency_field="currency_id",
        group_operator="sum",
        default=0.0,
        string="Amount per cycle",
    )
    amount_per_individual_in_group = fields.Monetary(
        currency_field="currency_id",
        group_operator="sum",
        default=0.0,
        string="Amount per individual in group",
    )
    max_individual_in_group = fields.Integer(
        default=0,
        string="Maximum number of individual in group",
        help="0 means no limit",
    )
    entitlement_validation_group_id = fields.Many2one(
        "res.groups", string="Payment Validation Group"
    )

    def create_program(self):
        # Set default program journal
        # journals = self.env["account.journal"].search(
        #    [("beneficiary_disb", "=", True), ("type", "in", ("bank", "cash"))]
        # )
        for rec in self:
            # if journals:
            #    journal_id = journals[0].id
            # else:
            # There are no default journals defined, create a new one
            journal_id = self.create_journal(rec.name, rec.currency_id.id)

            program = self.env["g2p.program"].create(
                {
                    "name": rec.name,
                    "journal_id": journal_id,
                }
            )
            program_id = program.id
            vals = {}

            # Set Default Eligibility Manager settings
            # Add a new record to default eligibility manager model
            def_mgr_obj = "g2p.program_membership.manager.default"
            def_mgr = self.env[def_mgr_obj].create(
                {
                    "name": "Default",
                    "program_id": program_id,
                    "eligibility_domain": rec.eligibility_domain,
                }
            )
            # Add a new record to eligibility manager parent model
            man_obj = self.env["g2p.eligibility.manager"]
            mgr = man_obj.create(
                {
                    "program_id": program_id,
                    "manager_ref_id": "%s,%s" % (def_mgr_obj, str(def_mgr.id)),
                }
            )
            vals.update({"eligibility_managers": [(4, mgr.id)]})

            # Set Default Cycle Manager settings
            # Add a new record to default cycle manager model
            def_mgr_obj = "g2p.cycle.manager.default"
            def_mgr = self.env[def_mgr_obj].create(
                {
                    "name": "Default",
                    "program_id": program_id,
                    "auto_approve_entitlements": rec.auto_approve_entitlements,
                    "cycle_duration": rec.cycle_duration,
                    "approver_group_id": rec.approver_group_id.id or None,
                }
            )
            # Add a new record to cycle manager parent model
            man_obj = self.env["g2p.cycle.manager"]
            mgr = man_obj.create(
                {
                    "program_id": program_id,
                    "manager_ref_id": "%s,%s" % (def_mgr_obj, str(def_mgr.id)),
                }
            )
            vals.update({"cycle_managers": [(4, mgr.id)]})

            # Set Default Entitlement Manager settings
            # Add a new record to default entitlement manager model
            def_mgr_obj = "g2p.program.entitlement.manager.default"
            def_mgr = self.env[def_mgr_obj].create(
                {
                    "name": "Default",
                    "program_id": program_id,
                    "amount_per_cycle": rec.amount_per_cycle,
                    "amount_per_individual_in_group": rec.amount_per_individual_in_group,
                    "max_individual_in_group": rec.max_individual_in_group,
                    "entitlement_validation_group_id": rec.entitlement_validation_group_id.id,
                }
            )
            # Add a new record to entitlement manager parent model
            man_obj = self.env["g2p.program.entitlement.manager"]
            mgr = man_obj.create(
                {
                    "program_id": program_id,
                    "manager_ref_id": "%s,%s" % (def_mgr_obj, str(def_mgr.id)),
                }
            )
            vals.update({"entitlement_managers": [(4, mgr.id)]})

            # Complete the program data
            program.update(vals)

            # Open the newly created program
            action = {
                "name": _("Programs"),
                "type": "ir.actions.act_window",
                "res_model": "g2p.program",
                "view_mode": "form,list",
                "res_id": program_id,
            }
            return action

    def close_wizard(self):
        return {"type": "ir.actions.act_window_close"}

    def create_journal(self, name, currency_id):
        program_name = name.split(" ")
        code = ""
        for pn in program_name:
            if pn:
                code += pn[0].upper()
        if len(code) == 0:
            code = program_name[3].strip().upper()
        account_chart = self.env["account.account"].search(
            [
                ("company_id", "=", self.env.company.id),
                ("user_type_id.type", "=", "liquidity"),
            ]
        )
        default_account_id = None
        if account_chart:
            default_account_id = account_chart[0].id
        new_journal = self.env["account.journal"].create(
            {
                "name": name,
                "beneficiary_disb": True,
                "type": "bank",
                "default_account_id": default_account_id,
                "code": code,
                "currency_id": currency_id,
            }
        )
        return new_journal.id
