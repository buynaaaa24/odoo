from email.policy import default


from odoo import fields, models, api, _
from odoo.tools.populate import compute


class Property(models.Model):
    _name = 'estate.property'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Зарагдах хөрөнгүүд'

    name = fields.Char(string="Name", required=True)
    state = fields.Selection([
        ('шинэ', 'Шинэ'),
        ('received', 'Offer received'),
        ('зөвшөөрсөн', 'Санал хүлээн зөвшөөрсөн'),
        ('зарагдсан', 'Зарагдсан'),
        ('цуцлах', 'Цуцлагдсан'),
        ('хүлээж авсан', 'Хүлээж авсан')  # Added this value
    ], default='шинэ', string='Status', group_expand='_expand_state')


    tag_ids = fields.Many2many('estate.property.tag', string="Бүтээгдэхүүний тэмдэг")
    type_id = fields.Many2one('estate.property.type',string="Бүтээгдэхүүний хэлбэр")
    description = fields.Text(string="Тайлбар")
    postcode = fields.Text(string="Посскод")
    date_availability = fields.Date(string="Хугацаа")
    expected_price = fields.Monetary(string="Хүссэн үнэ", tracking=True)
    best_offer = fields.Monetary(string="Санал болгох үнэ", compute='_compute_best_price')
    selling_price = fields.Monetary(string="Зарах үнэ", readonly=True)
    bedrooms = fields.Integer(string="Унтлагийн өрөө")
    living_area = fields.Integer(string="Өрөөний хэмжээ(м.кв)")
    facade = fields.Integer(string="facade")
    garage = fields.Boolean(string="Гараж", default=False)
    garden = fields.Boolean(string="Цэцэрлэг", default=False)
    garden_area = fields.Integer(string="Цэцэрлэгийн талбай(м.кв)")
    garden_orientation = fields.Selection(
        [('north','NORTH'),('south','SOUTH'),('west','WEST'),('east','EAST')],
        string="Garden Orientation",default='north')
    offer_ids = fields.One2many('estate.property.offer','property_id', string="Саналууд")
    sales_id = fields.Many2one('res.users', string="Агент")
    buyer_id = fields.Many2one('res.partner', string="Худалдан авагч")
    phone = fields.Char(string="Утас", related='buyer_id.phone')
    currency_id = fields.Many2one("res.currency", string="Ханш",
                                  default=lambda self: self.env.user.company_id.currency_id)

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    total_area = fields.Integer(string="Нийт хэмжээ", compute='_compute_total_area')

    def action_sold(self):
        self.state = 'зарагдсан'

    def action_cancel(self):
        self.state = 'цуцлах'



    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for rec in self:
            rec.offer_count = len(rec.offer_ids)

    offer_count = fields.Integer(string="Offer Count", compute=_compute_offer_count)

    def action_property_view_offers(self):
        return {
            'type': 'ir.actions.act_window',
            'name': f"{self.name} - Offers",
            'domain': [('property_id', '=', self.id)],
            'view_mode': 'tree',
            'res_model': 'estate.property.offer',
        }

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for rec in self:
            if rec.offer_ids:
                rec.best_offer = max(rec.offer_ids.mapped('price'))
            else:
                rec.best_offer=0

    def action_url_action(self):
        return {
            'type': 'ir.actions.act_url',
            'url': 'https://www.realtor.com/realestateandhomes-search/Minneapolis_MN/show-newest-listings/sby-6',
            'target': 'new',
        }
    def _get_report_base_filename(self):
        self.ensure_one()
        return 'Estate Property - %s' % self.name

    # def _compute_website_url(self):
    #     for rec in self:
    #         rec.website_url = "/properties/%s" % rec.id

    def action_send_email(self):
        mail_template = self.env.ref('real_estate_ads.offer_mail_template')
        mail_template.send_mail(self.id, force_send=True)

    # def _get_emails(self):
    #     return ','.join(self.offer_ids.mapped('partner_email'))

    def _expand_state(self, states, domain, order):
        return[
            key for key, dummy in type(self).state.selection
        ]


class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Бүтээгдэхүүний төрлүүд'

    name = fields.Char(string="Name", required=True)


class PropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Бүтээгдэхүүний тэмдэг'

    name = fields.Char(string="Нэр", required=True)
    color = fields.Integer(string="Color")