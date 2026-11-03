from odoo import fields, models, api
from odoo.exceptions import ValidationError


class HospitalCanteen(models.Model):
    _name = "hospital.canteen"
    _description = "Hospital Canteen"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "food_name"

    food_name = fields.Char(
        string="Food Name",
        required=True,
    )

    food_manufacture_date = fields.Date(
        string="Food Manufacture Date",
        required=True,
    )

    gender = fields.Selection(
        selection=[
            ("male", "Male"),
            ("female", "Female"),
        ],
        string="Gender",
        required=True,
    )

    people_type = fields.Selection(
        selection=[
            ("doctor", "Doctor"),
            ("patient", "Patient"),
            ("nurse", "Nurse"),
            ("wordboy", "Wordboy"),
            ("ambulance driver", "Ambulance Driver"),
            ("other", "Other"),
        ],
        string="People Type",
        required=True,
    )

    quantity = fields.Float(
        string="Quantity",
        default=1.0,
        required=True,
    )

    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        default=lambda self: self.env.company.currency_id,
        required=True,
    )

    unit_price = fields.Monetary(
        string="Unit Price",
        currency_field="currency_id",
        required=True,
    )

    tax_percent = fields.Float(
        string="Tax (%)",
        default=0.0,
    )

    subtotal = fields.Monetary(
        string="Subtotal",
        compute="_compute_price",
        store=True,
        currency_field="currency_id",
    )

    tax_amount = fields.Monetary(
        string="Tax Amount",
        compute="_compute_price",
        store=True,
        currency_field="currency_id",
    )

    total_price = fields.Monetary(
        string="Total Price",
        compute="_compute_price",
        store=True,
        currency_field="currency_id",
    )

    progress = fields.Float(
        string="Progress",
        default=0.0,
    )

    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("active", "Active"),
            ("done", "Done"),
            ("cancel", "Cancel"),
        ],
        string="Status",
        default="draft",
        required=True,
        tracking=True,
    )

    @api.depends("quantity", "unit_price", "tax_percent", "currency_id")
    def _compute_price(self):
        for record in self:
            currency = record.currency_id

            subtotal = record.quantity * record.unit_price
            record.subtotal = currency.round(subtotal)

            tax = record.subtotal * record.tax_percent / 100
            record.tax_amount = currency.round(tax)

            record.total_price = record.subtotal + record.tax_amount

    @api.constrains("quantity", "unit_price", "tax_percent")
    def _check_price(self):
        for record in self:
            if record.quantity <= 0:
                raise ValidationError("Quantity 0 er beshi hote hobe.")

            if record.unit_price < 0:
                raise ValidationError("Unit price negative hote parbe na.")

            if record.tax_percent < 0 or record.tax_percent > 100:
                raise ValidationError("Tax 0 theke 100 er vitor hobe.")

    def action_confirm(self):
        for record in self:
            record.state = "active"

    def action_done(self):
        for record in self:
            record.state = "done"
            record.progress = 100.0

    def action_cancel(self):
        for record in self:
            record.state = "cancel"
            record.progress = 0.0

    def action_draft(self):
        for record in self:
            record.state = "draft"
            record.progress = 0.0

    @api.onchange("food_name")
    def _onchange_methods(self):
        if self.food_name:
            if not self.food_manufacture_date:
                self.food_manufacture_date=fields.Date.today()


