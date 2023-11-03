# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountChequePayment(models.Model):
    _name = "account.cheque_payment"
    _inherit = ["account.cheque_payment"]

    payment_order_ids = fields.One2many(
        string="Payment Orders",
        comodel_name="payment_order",
        inverse_name="cheque_payment_id",
    )
    payment_order_id = fields.Many2one(
        string="# Payment Order",
        comodel_name="payment_order",
        compute="_compute_payment_order_id",
        store=True,
    )

    @api.depends(
        "payment_order_ids",
    )
    def _compute_payment_order_id(self):
        for record in self:
            result = False
            if record.payment_order_ids:
                result = record.payment_order_ids[0]
            record.payment_order_id = result

    def _prepare_account_move(self):
        self.ensure_one()
        _super = super(AccountChequePayment, self)
        result = _super._prepare_account_move()
        result.update(
            {
                "payment_order_id": self.payment_order_id.id,
            }
        )
        return result
