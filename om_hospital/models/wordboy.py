from odoo import fields, models


class WordBoy(models.Model):
    _name = "wordboy"
    _description = "WordBoy"
    _inherit=["mail.thread","mail.activity.mixin"]

    # WordBoy er naam
    name = fields.Char(
        string="Name",
        required=True,
    )

    # Chobi upload korar field and pic er height 1040  and max height 1040

    image = fields.Image(
        string="Photo",
        max_width=1040,
        max_height=1040,
    )

    #  phone number
    phone = fields.Char(
        string="Phone Number",
        required=True,
    )

    # Bashar thikana
    address = fields.Char(
        string="Address",
        required=True,
    )

    # Kaj e jog dewar date

    joining_date = fields.Date(
        string="Joining Date",
        default=fields.Date.context_today,
    )

    # Joruri proyojone jar sathe jogajog kora hobe tar naam
    emergency_contact_name = fields.Char(
        string="Emergency Contact Name",
    )

    # Joruri contact phone number
    emergency_contact_phone = fields.Char(
        string="Emergency Contact Phone",
    )

    # Jogajoger bektir sathe shomporko
    emergency_contact_relation = fields.Char(
        string="Relationship",
    )

    # emergency contract number
    emergency_contract_number = fields.Char(
        string="Emergency Contract Number",
        required=True,
        default="01712155351",
    )

    # WordBoy er registration number
    registration_number = fields.Integer(
        string="WordBoy Registration Number",
        required=True,
    )

    # Priority select korar option
    priority = fields.Selection(
        selection=[
            ("0", "Normal"),
            ("1", "Low"),
            ("2", "Medium"),
            ("3", "High"),
        ],
        string="Priority",
        required=True,
        default="0",
    )

    # Record er bortoman obostha default draft e thakbe

    state = fields.Selection(  # selection field
        selection=[
            ("draft", "Draft"),
            ("done", "Done"),
        ],
        string="State",    # string state
        required=True,     # required true means ei field add kortei hbe
        default="draft",   #draft obosthai draft hbe

    )
    partner_id=fields.Many2one(
        comodel_name="res.partner",
        string="Contact"
    )
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Responsible User",
        default=lambda self: self.env.user, #new record korar somoy kar name ache automatically bosbe
        domain=[("share", "=", False)], #user seletion just internal user dekhbe
        tracking=True,
    )

    #select korbe sales order

    sale_order_id = fields.Many2one(
        comodel_name="sale.order", # onno model er sathe relationship build up korche sale.order er sathe
        string="Sales Order",
        groups="sales_team.group_sale_salesman", # sales group er user field acess korte parbe
    )

    sale_customer_id = fields.Many2one(
        related="sale_order_id.partner_id",  # sales order id theke customer er info niye asbe
        string="Sales Customer",
        readonly=True,  #just read korte parbe edit korte parbe na
        related_sudo=False,
        groups="sales_team.group_sale_salesman", #just sales group er member ra eita use access korte parbe
    )

    sale_order_date = fields.Datetime(
        related="sale_order_id.date_order", # sales order id and oi order er date
        string="Sales Order Date",
        readonly=True,
        related_sudo=False, #oi sales order porar permission ache kina ?
        groups="sales_team.group_sale_salesman",
    )
    def action_confirm(self):
        for record in self:
            record.state = "done"

        # Confirm korar por animation dekhabe
        return {
            "effect": {
                "type": "rainbow_man",
                "message": "Congratulations! WordBoy is completed! 🎉",
                "fadeout": "fast",
            }
        }

    # Reset button e click korle abar Draft hobe
    def action_reset(self):
        for record in self:
            record.state = "draft"