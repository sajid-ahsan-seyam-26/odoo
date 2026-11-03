from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order" # inherit korbe sale.order

    confirmed_user_id = fields.Many2one(
        comodel_name="res.users",
        string="Confirmed User",
    )

    patient_id = fields.Many2one(
        comodel_name="hospital.patient", #comodel name holo targeted model theke data niye asbe for example patient
        string="Patient",
        ondelete="restrict",   # sale field theke kono patient delete korte parbe na
    )

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    extra_item = fields.Char(string="Extra Item") # extra item add kora

    payment_method = fields.Selection(    # selection field theke ki method e payment korbe seta
        selection=[
            ("cash", "Cash"),
            ("online", "Online"),
            ("card", "Card"),
        ],
        string="Payment",
    )