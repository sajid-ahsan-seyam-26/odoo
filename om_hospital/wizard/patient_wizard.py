from odoo import fields, models


class HospitalPatientWizard(models.TransientModel):
    _name = "hospital.patient.wizard"
    _description = "Assign Patient WordBoy"

    patient_id = fields.Many2one(
        "hospital.patient",
        string="Patient",
        required=True,
    )

    wordboy_id = fields.Many2one(
        "wordboy",
        string="WordBoy",
        required=True,
    )

    def action_confirm(self):
        self.ensure_one()

        # Selected WordBoy Patient-er Record e save korbe
        self.patient_id.write({
            "wordboy_id": self.wordboy_id.id,
        })

        # Save save houyar por pop up off hbe
        return {
            "type": "ir.actions.act_window_close",
        }

    def action_print_pdf(self):
        self.ensure_one()

        # report action khujbe
        report = self.env.ref(
            "om_hospital.action_report_patient_wordboy"
        )

        # pdf report toiri korbe
        return report.report_action(self)


class HospitalPatient(models.Model):
    _inherit = "hospital.patient"

    def action_open_wizard(self):
        self.ensure_one()

        # selected patiend er wizard khulbe
        return {
            "type": "ir.actions.act_window",
            "name": "Assign WordBoy",
            "res_model": "hospital.patient.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                **self.env.context,
                "default_patient_id": self.id,
                "default_wordboy_id": self.wordboy_id.id,
            },
        }