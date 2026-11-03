from odoo import fields, models

class Seyam(models.Model):
    _name="seyam"
    _description="seyam"


    name=fields.Char(
        string="Name",
        required=True,
        index=True,
        copy=True,

    )
    employee_id=fields.Integer(
        string="Employee ID",
        index=True,
        copy=True,
        required=True,
    )
    position = fields.Char(
        string="Position",
        required=True,
        readonly=True,
        copy=True
    )
    postcode=fields.Integer(
        string="postcode",
        readonly=True,
        index=True,
        copy=True,
        required=True,
    )