# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class PaymentOrder(models.Model):
    _name = "payment_order"
    _inherit = ["payment_order"]

    bank_payment_id = fields.Many2one(
        string="# Bank Voucher",
        comodel_name="account.bank_payment",
    )

    cash_payment_id = fields.Many2one(
        string="# Cash Voucher",
        comodel_name="account.cash_payment",
    )

    @api.model
    def _get_realization_field(self):
        _super = super(PaymentOrder, self)
        result = _super._get_realization_field()
        result += [
            "bank_payment_id",
            "cash_payment_id",
        ]
        return result

    def _create_realization_bank(self):
        self.ensure_one()
        BP = self.env["account.bank_payment"]
        bank_payment = BP.create(self._prepare_bank_voucher_header())
        self.write(
            {
                "bank_payment_id": bank_payment.id,
            }
        )

        for payment_request in self.payment_request_ids:
            payment_request._create_realization_bank()

    def _create_realization_cash(self):
        self.ensure_one()
        CP = self.env["account.cash_payment"]
        cash_payment = CP.create(self._prepare_cash_voucher_header())
        self.write(
            {
                "cash_payment_id": cash_payment.id,
            }
        )

        for payment_request in self.payment_request_ids:
            payment_request._create_realization_cash()

    def _prepare_bank_voucher_header(self):
        self.ensure_one()
        result = self._prepare_voucher_header()
        result.update(
            {
                "type_id": self.env.ref(
                    "ssi_voucher_bank_cash.voucher_type_bank_payment"
                ).id,
            }
        )
        return result

    def _prepare_cash_voucher_header(self):
        self.ensure_one()
        result = self._prepare_voucher_header()
        result.update(
            {
                "type_id": self.env.ref(
                    "ssi_voucher_bank_cash.voucher_type_cash_payment"
                ).id,
            }
        )
        return result

    def _prepare_voucher_header(self):
        self.ensure_one()
        return {
            "name": "/",
            "date_voucher": self.date,
            "journal_id": self.type_id.journal_id.id,
            "account_id": self.type_id.journal_id.default_account_id.id,
            "amount": self.amount_request,
            "description": self.name,
        }
