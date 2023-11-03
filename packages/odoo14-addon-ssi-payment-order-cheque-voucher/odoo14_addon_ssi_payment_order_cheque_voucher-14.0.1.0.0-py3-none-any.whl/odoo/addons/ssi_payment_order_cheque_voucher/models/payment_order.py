# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PaymentOrder(models.Model):
    _name = "payment_order"
    _inherit = ["payment_order"]

    cheque_payment_id = fields.Many2one(
        string="# Cheque Voucher",
        comodel_name="account.bank_payment",
    )

    def _create_realization_cheque(self):
        self.ensure_one()
        CP = self.env["account.cheque_payment"]
        cheque_payment = CP.create(self._prepare_cheque_voucher_header())
        self.write(
            {
                "cheque_payment_id": cheque_payment.id,
            }
        )

        for payment_request in self.payment_request_ids:
            payment_request._create_realization_cheque()

    def _prepare_voucher_header(self):
        self.ensure_one()
        return {
            "name": "/",
            "date_voucher": self.date,
            "journal_id": self.type_id.journal_id.id,
            "account_id": self.type_id.journal_id.default_account_id.id,
            "amount": self.amount_request,
            "description": self.name,
            "type_id": self.env.ref(
                "ssi_voucher_cheque.voucher_type_cheque_payment"
            ).id,
        }
