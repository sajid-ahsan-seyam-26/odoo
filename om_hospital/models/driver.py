from odoo import fields, models,api
class driver(models.Model):
    _name = "hospital.driver"
    _description="Driver"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name=fields.Char(
        string="Driver name",
        required=True,

    )
    phone_number=fields.Char(
        string="phone Number",
        required=True,
    )

    ambulance_type=fields.Selection(
        selection=[
            ("hino ambulance","Hino ambulance"),
            ("toyota ambulance","Toyota ambulance"),
            ("hundai ambulance","Hundai ambulance"),

        ],
        string="Ambulance Type",
        required=True,
    )

    total_km=fields.Float(
        string="Total KM",
        required=False,
    )
    rate_per_km=fields.Float(
        string="Rate per KM",
        default=10.0,
        required=True,
    )
    total_fare=fields.Float(
        string="Total Fare Tk",
        required=False,
        compute="_compute_total_fare",
        store=True,


    )

    color=fields.Integer(
        string="color",
        default=0,
    )


    state=fields.Selection(
        selection=[
            ("draft","Draft"),
            ("confirmed","Confirmed"),
        ],
        string="Sate",
        default="draft",
        required=True,
    )
    def action_confirm(self):
        for record in self:
            record.state="confirmed"
    def action_draft(self):
        for record in self:
            record.state="draft"

    @api.depends("total_km", "rate_per_km")
    def _compute_total_fare(self):
        for record in self:
            record.total_fare = (
                    record.total_km * record.rate_per_km
            )








