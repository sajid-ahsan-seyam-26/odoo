from odoo.tests.common import TransactionCase
from odoo.tools.safe_eval import safe_eval


class TestDoctorSelection(TransactionCase):
    def test_selection_and_reassignment(self):
        users = self.env['res.users'].create([
            {'name': 'Selection Doctor A', 'login': 'selection_doctor_a'},
            {'name': 'Selection Doctor B', 'login': 'selection_doctor_b'},
        ])
        doctors = self.env['hospital_doctor'].create([
            {
                'name': user.name,
                'doctor_code': user.login,
                'registration_number': user.login,
                'specialization': 'general',
                'user_id': user.id,
            }
            for user in users
        ])
        patient = self.env['hospital.patient'].create({
            'name': 'Selection Patient',
            'date_of_birth': '2000-01-01 00:00:00',
            'age': 26,
            'phone': '0123456789',
            'email': 'selection@example.com',
            'address': 'Test address',
            'notes': 'Test consultation',
            'doctor_id': doctors[0].id,
        })
        action = self.env.ref('om_hospital.action_hospital_my_patients')

        def my_patients(user):
            domain = safe_eval(action.domain, {'uid': user.id})
            return self.env['hospital.patient'].search(domain)

        self.assertIn(patient, doctors[0].patient_ids)
        self.assertIn(patient, my_patients(users[0]))
        self.assertNotIn(patient, my_patients(users[1]))
        patient.doctor_id = doctors[1]
        self.assertNotIn(patient, doctors[0].patient_ids)
        self.assertIn(patient, doctors[1].patient_ids)
        self.assertNotIn(patient, my_patients(users[0]))
        self.assertIn(patient, my_patients(users[1]))
        patient.doctor_id = False
        self.assertNotIn(patient, my_patients(users[1]))
