from odoo import fields, models


class HospitalDoctor(models.Model):
    _name = "hospital_doctor"
    _description = "Hospital Doctor"
    _order = "name"

    name = fields.Char(
        string="Doctor Name",
        required=True,
    )

    doctor_code = fields.Char(
        string="Doctor ID",
        required=True,
        copy=False,
    )


    specialization = fields.Selection(
        [
            ("general", "General Medicine Dmc"),
            ("cardiology", "Cardiology"),
            ("neurology", "Neurology"),
            ("orthopedics", "Orthopedics"),
            ("pediatrics", "Pediatrics"),
            ("dermatology", "Dermatology"),
            ("gynecology", "Gynecology"),
            ("surgery", "Surgery"),
        ],
        string="Specialization",
        required=True,
    )

    qualification = fields.Char(
        string="Qualification",
    )

    registration_number = fields.Char(
        string="Medical Registration No.",
        required=True,
    )

    phone = fields.Char(
        string="Phone",
    )

    email = fields.Char(
        string="Email",
    )

    experience = fields.Integer(
        string="Experience (Years)",
    )

    consultation_fee = fields.Float(
        string="Consultation Fee",
    )

    joining_date = fields.Date(
        string="Joining Date",
        default=fields.Date.today,
    )

    notes = fields.Text(
        string="Notes",
    )

    user_id = fields.Many2one(
        "res.users",
        string="Login User",
        copy=False,
        index=True,
        domain=[("share", "=", False)],
        help="The internal account this doctor uses to view My Patients.",
    )

    patient_ids = fields.One2many(
        "hospital.patient",
        "doctor_id",
        string="Patients",
        readonly=True,
    )
