# Copyright 2015 Omar Castiñeira, Comunitea Servicios Tecnológicos S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Partial Payment Reconcile",
    "version": "15.0.1.0.0",
    "author": "Comunitea, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/sale-workflow",
    "category": "Sales",
    "license": "AGPL-3",
    "summary": "Allow to add advance payments on sales and then use them on invoices",
    "depends": ["sale","account_accountant"],
    "data": [
        "wizard/sale_advance_payment_wzd_view.xml",
        "views/account_payment_view.xml",
        "views/sale_view.xml",
        'views/manual_reconciliation_line.xml',
        "security/ir.model.access.csv",
    ],
    'assets': {
        'web.assets_backend':[
            'sale_advance_payment/static/src/js/account_payment_field.js',
        ],},
    "installable": True,
}
