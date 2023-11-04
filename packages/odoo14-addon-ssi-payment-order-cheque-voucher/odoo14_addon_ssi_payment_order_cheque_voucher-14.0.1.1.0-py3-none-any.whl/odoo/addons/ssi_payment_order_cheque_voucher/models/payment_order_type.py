# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PaymentOrderType(models.Model):
    _name = "payment_order_type"
    _inherit = [
        "payment_order_type",
    ]

    realization_method = fields.Selection(
        selection_add=[
            ("cheque", "Cheque Payment"),
        ],
        ondelete={
            "cheque": "set default",
        },
    )
