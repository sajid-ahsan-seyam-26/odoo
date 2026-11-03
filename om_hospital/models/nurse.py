from odoo import api, fields, models


class Nurse(models.Model):
    _name = "hospital.nurse"
    _description = "Nurse"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    priority = fields.Selection(
        selection=[
            ("0", "Normal"),
            ("1", "Low"),
            ("2", "High"),
            ("3", "Very High"),
        ],
        string="Priority",
        default="0",
    )

    name = fields.Char(
        string="Name",
        required=True,
        tracking=True,
    )

    date_of_birth = fields.Date(
        string="Date of Birth",
        required=True,
        tracking=True,
    )

    age = fields.Integer(
        string="Age",
        compute="_compute_age",
        readonly=True,
        store=False,
    )

    gender = fields.Selection(
        selection=[
            ("male", "Male"),
            ("female", "Female"),
            ("other", "Other"),
        ],
        string="Gender",
        default="male",
        tracking=True,
    )

    registration = fields.Char(
        string="Registration No",
        required=True,
        tracking=True,
    )

    nurse_code = fields.Char(
        string="Nurse Code",
        required=True,
        tracking=True,
    )

    notes = fields.Html(
        string="Notes",
        sanitize=True,
    )

    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("active", "Active"),
            ("inactive", "Inactive"),
        ],
        string="Status",
        default="draft",
        tracking=True,
        required=True,
    )
    currency_id=fields.Many2one(
        "res.currency",
        string="currency",
        default=lambda self:self.env.company.currency_id,

        required=True,

    )
    salary=fields.Monetary(
        string="salary",
        currency_field="currency_id",
        tracking=True,
    )


    @api.depends("date_of_birth")
    def _compute_age(self):
        today = fields.Date.today()

        for record in self:
            if record.date_of_birth:
                dob = record.date_of_birth

                years = (
                    today.year
                    - dob.year
                    - ((today.month, today.day) < (dob.month, dob.day))
                )

                record.age = max(years, 0)
            else:
                record.age = 0

    def action_activate(self):
        self.write({
            "state": "active"
        })

    def action_deactivate(self):
        self.write({
            "state": "inactive"
        })

    def action_draft(self):
        self.write({
            "state": "draft"
        })