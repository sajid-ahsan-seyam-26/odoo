from odoo import fields, models,api
from odoo.exceptions import ValidationError,UserError


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "Hospital Patient"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(
        string="Name",
        required=True,
        tracking=True,
    )

    date_of_birth = fields.Datetime(
        string="Date of Birth",
        required=True,
        tracking=True,
    )

    age = fields.Integer(
        string="Age",
        compute="compute_age",
        required=True,
        tracking=True,
    )

    gender = fields.Selection(
        selection=[
            ("male", "Male"),
            ("female", "Female"),
            ("other", "Other"),
        ],
        string="Gender",
        tracking=True,
    )

    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("active", "Active"),
        ],
        string="State",
        default="draft",
        tracking=True,
    )

    phone = fields.Char(required=True, tracking=True)
    email = fields.Char(required=True, tracking=True)
    address = fields.Char(required=True, tracking=True)
    notes = fields.Text(required=True, tracking=True)
    active = fields.Boolean(default=True, tracking=True)

    doctor_id = fields.Many2one(
        "hospital_doctor",
        string="Doctor",


        tracking=True,
        help="Select the doctor this patient wants to consult.",
    )
    wordboy_id = fields.Many2one(
        "wordboy",
        string="WordBoy",
        tracking=True,

    )

    def action_activate(self):
        self.write({"state": "active"})
        return True

    def action_reset(self):
        self.write({"state": "draft"})
        return True



    @api.depends("date_of_birth")
    def compute_age(self):
        today = fields.Date.today()
        for record in self:
            if record.date_of_birth:
                dob = fields.Date.to_date(record.date_of_birth) #date of birth k date e convert kore dob te rakhe
                record.age = today.year - dob.year - (
                        (today.month, today.day) < (dob.month, dob.day)
                )
            else:
                record.age = 0

    @api.constrains("date_of_birth")
    def check_date_of_birth(self):
        today = fields.Date.today()

        for record in self:
            if record.date_of_birth:
                dob = fields.Date.to_date(record.date_of_birth)

                if dob == today:
                    raise ValidationError(
                        "Birthday ajker date hote parbe na/0"
                    )
                elif dob > today:
                    raise ValidationError(
                        "birthday infuture hote parbe na /-1 "
                    )

    @api.onchange("email")
    def _onchange_email(self):

        for record in self:
            if record.email:
                email = record.email # record e thaka email gulo email variable e ana
                email = email.strip() # first and last er space remove
                email = email.lower() # uppercase thakle lowercase
                email=email.replace(" ","") # vitorer space remove korbe
                record.email = email

    @api.constrains("name")
    def _check_name(self):
        for record in self:
            if record.name:
                for char in record.name:
                    if char.isdigit():
                        raise UserError("name er vetor kono digit thakte parbe na")




