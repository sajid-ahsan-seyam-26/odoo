from odoo import api, fields, models, _
from odoo.exceptions import AccessError


class HospitalAdmin(models.Model):
    _name = "hospital.admin"
    _description = "Hospital Administrator"
    _order = "name"

    name = fields.Char(string="Administrator Name", required=True)
    phone = fields.Char()
    email = fields.Char()
    active = fields.Boolean(default=True)
    notes = fields.Text()

    patient_count = fields.Integer(compute="_compute_counts")
    doctor_count = fields.Integer(compute="_compute_counts")
    nurse_count = fields.Integer(compute="_compute_counts")
    staff_count = fields.Integer(compute="_compute_counts")

    @api.depends_context("uid")   # je id te log in kora
    def _compute_counts(self):
        counts = {
            "patient_count": self.env["hospital.patient"].search_count([]),   # hospital model e jabe and patient count korbe
            "doctor_count": self.env["hospital_doctor"].search_count([]),     #self.env holo oi model gulai access pauyar way
            "nurse_count": self.env["hospital.nurse"].search_count([]),
            "staff_count": self.env["seyam"].search_count([]),
        }
        for record in self:
            for field, count in counts.items():
                record[field] = count

    def _open_hospital_action(self, xml_id):
        self.ensure_one()     # oddo te ekta record ei thake
        if not self.env.user.has_group("om_hospital.group_hospital_admin"):    # jodi admin thake tahole seta security file e check korbe otherwise false hole acces pabe na
            raise AccessError(
                _("Only hospital administrators can use these controls.")
            )
        return self.env["ir.actions.actions"]._for_xml_id(xml_id)

    def action_open_patients(self):
        return self._open_hospital_action(
            "om_hospital.action_hospital_patient"
        )

    def action_open_doctors(self):
        return self._open_hospital_action(
            "om_hospital.action_hospital_doctor"
        )

    def action_open_nurses(self):
        return self._open_hospital_action("om_hospital.action_nurse")

    def action_open_staff(self):
        return self._open_hospital_action("om_hospital.action_seyam")