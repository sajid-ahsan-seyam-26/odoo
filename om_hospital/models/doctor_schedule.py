from odoo import fields, models


class HospitalDoctorSchedule(models.Model):
    _name = "hospital.doctor.schedule"
    _description = "Doctor Schedule"
    _order = "date_start"

    name = fields.Char(
        string="Task", # task assign korar jonno ekta
        required=True,
    )

    doctor_id = fields.Many2one(
        "hospital_doctor",  # many to one mathod use kora hoyeche karon ekta schedule ekjon doctor er jonnoi
        string="Doctor",
        required=True,
    )

    date_start = fields.Datetime(            # start time
        string="Start Time",
        required=True,
    )

    date_end = fields.Datetime(                # end time
        string="End Time",
        required=True,
    )