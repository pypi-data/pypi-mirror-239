# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Payment Order + Cash Bank Voucher",
    "version": "14.0.1.0.0",
    "category": "Accounting",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_payment_order",
        "ssi_voucher_bank_cash",
    ],
    "data": [
        "views/payment_order_views.xml",
        "views/bank_payment_views.xml",
        "views/cash_payment_views.xml",
    ],
    "demo": [],
    "images": [],
}
