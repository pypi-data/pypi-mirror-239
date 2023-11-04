# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class PaymentRequest(models.Model):
    _name = "payment_request"
    _inherit = ["payment_request"]

    def _create_realization_cheque(self):
        self.ensure_one()

        Line = self.env["account.cheque_payment_line"]
        Line.create(self._prepare_cheque_realization())

    def _prepare_cheque_realization(self):
        self.ensure_one()
        ml = self.move_line_id
        return {
            "voucher_id": self.payment_order_id.cheque_payment_id.id,
            "account_id": ml.account_id.id,
            "move_line_id": ml.id,
            "partner_id": self.partner_id.id,
            "name": ml.name or self.payment_order_id.name,
            "amount": self.amount_payment,
            "type": "dr",
        }
