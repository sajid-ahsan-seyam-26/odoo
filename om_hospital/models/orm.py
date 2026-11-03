from odoo import models, fields


class HospitalOrm(models.Model):
    _name = "hospital.orm"
    _description = "ORM Practice"
    _rec_name = "driver_record_id"

    driver_record_id = fields.Integer(string="Driver ID")
    search_name = fields.Char(string="Search Name")
    result = fields.Text(readonly=True)

    def action_create(self):
        self.ensure_one()
        # driver veriable e rakhbe new driver jeta create hbe
        driver = self.env["hospital.driver"].create({
            "name": "OGGY",
            "phone_number": "01712155351",
            "ambulance_type": "toyota ambulance",
        })

        self.driver_record_id = driver.id #new database id driver id te bosabe
        self.result = str(driver.id) + driver.name   #ei formet e taakbe 12OGGY
    # Browse()
    def action_browse(self):
        self.ensure_one()

        driver = self.env["hospital.driver"].browse(
            self.driver_record_id
        )

        self.result = str(driver.id) + driver.name

    def action_write(self):
        self.ensure_one()
        # driver information update korbe
        self.env["hospital.driver"].browse(self.driver_record_id).write({
            "name": "F1 Driver",
            "total_km": 70.0,
        })

        self.result = "Driver update kora hoyeche."
   # delete korbe driver info
    def action_unlink(self):
        self.ensure_one()

        self.env["hospital.driver"].browse(
            self.driver_record_id
        ).unlink()

        self.driver_record_id = 0
        self.result = "Driver delete kora hoyeche."

    def action_get_metadata(self):
        self.ensure_one()

        driver = self.env["hospital.driver"].browse(
            self.driver_record_id
        ).get_metadata()

        self.result = str(driver)

    def action_search(self):
        self.ensure_one()

        drivers = self.env["hospital.driver"].search([
            ("name", "ilike", self.search_name ),
        ])

        self.result = str(drivers.read(["name", "phone_number"]))  # oi name diye pauya info theke name and phone number nibe

    def action_search_count(self):
        self.ensure_one()

        count = self.env["hospital.driver"].search_count([
            ("name", "ilike", self.search_name)
        ])

        self.result = "Total: " + str(count)            # search count korbe