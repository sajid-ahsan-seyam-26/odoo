from odoo import models,fields,api
from odoo.exceptions import ValidationError

class HospitalHelicopter(models.Model):
    _name="hospital.helicopter"
    _description = "Hospital Helicopter"


    name=fields.Char(
        string="helicopter name",
        required=True,
    )
    phone=fields.Char(
        string="phone number",
        required=True,
    )
    email=fields.Char(
        string="Email address",
    )

    helicopter=fields.Selection(
        selection=[
            ("Bell Huey","Bell Huey"),
            ("eurocopter Dolphin","Eurocopter Dolphin"),
            ("mi mil-17","Mi-mil-17"),
            ("robinson bell 121","robinson bell 121"),
        ],
        string="helicopter name",
        default="Bell Huey",
    )
    state=fields.Selection(
        selection=[
            ("active","Active"),
            ("draft","Draft"),
        ],
        string="helicopter state",
        default="draft",
    )
    hourly_rate=fields.Float(
        string="Hourly  rate",
    )
    rental_rate=fields.Float(
        string="Rental rate",
    )
    total_cost=fields.Float(
        string="Total cost",
        compute="_compute_total_cost",
        store=True,
    )


    def action_active(self):
        for record in self:
            record.state="active"
    def action_draft(self):
        for record in self:
            record.state="draft"

    def action_open_website(self):
        return {
            'type': 'ir.actions.act_url',   #url open korbe
            'url': 'https://www.bashundharaairways.com/',   #website of the url
            'target': 'new',   #window te ekta new tab khulbe
        }
    def action_video(self):
        return{
            'type': 'ir.actions.act_url',
            'url':'https://youtube.com/shorts/QlZZbDBTKuw?si=gcadYhgqyndqK3uw',
            'target': 'new',
        }
    def action_helicopter(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'message': 'Helicopter button has been clicked',
            }
        }
    def action_send_email(self):
        return {
            'type': 'ir.actions.act_url',
            'url': 'https://mail.google.com/mail/u/0/?view=cm&fs=1&to=' + (self.email or ''),
            'target': 'new',
        }


    def action_share_whatsapp(self):
        self.ensure_one()

        if not self.phone:
            raise ValidationError("Please enter a WhatsApp number.")

        phone = self.phone

        message = "Hello, helicopter rent and details info amk bolen kindly"
        whatsapp_api_url = 'https://api.whatsapp.com/send?phone=%s&text=%s' % (
            self.phone,
            message,
        )

        return {
            'type': 'ir.actions.act_url',
            'url': whatsapp_api_url,
            'target': 'new',
        }

    @api.depends("hourly_rate","rental_rate","total_cost")
    def _compute_total_cost(self):
        for record in self:
            record.total_cost=record.hourly_rate + record.rental_rate
