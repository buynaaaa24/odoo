from email.policy import default


from odoo import fields, models, api, _
from odoo.tools.populate import compute


class Property(models.Model):
    _name = 'estate.property'
    _description = 'Зарагдах хөрөнгүүд'

    name = fields.Char(string="Name", required=True)
    state = fields.Selection([
        ('шинэ', 'Шинэ'),
        ('received', 'Offer received'),
        ('зөвшөөрсөн', 'Санал хүлээн зөвшөөрсөн'),
        ('зарагдсан', 'Зарагдсан'),
        ('цуцлах', 'Цуцлагдсан'),
        ('хүлээж авсан', 'Хүлээж авсан')  # Added this value
    ], default='шинэ', string='Status')


    tag_ids = fields.Many2many('estate.property.tag', string="Бүтээгдэхүүний тэмдэг")
    type_id = fields.Many2one('estate.property.type',string="Бүтээгдэхүүний хэлбэр")
    description = fields.Text(string="Тайлбар")
    postcode = fields.Text(string="Посскод")
    date_availability = fields.Date(string="Хугацаа")
    expected_price = fields.Float(string="Хүссэн үнэ")
    best_offer = fields.Float(string="Санал болгох үнэ", compute='_compute_best_price')
    selling_price = fields.Float(string="Зарах үнэ", readonly=True)
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


    @api.onchange('living_area','garden_area')
    def _onchange_total_area(self):
        self.total_area = self.living_area + self.garden_area

    total_area = fields.Integer(string="Нийт хэмжээ",compute=_onchange_total_area)

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
            'name': f"{self.name} - 'Offers",
            'domain':[('property_id', '=', self.id)],
            'view_mode': 'tree',
            'view mode': 'tree',
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


class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Бүтээгдэхүүний төрлүүд'

    name = fields.Char(string="Name", required=True)


class PropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Бүтээгдэхүүний тэмдэг'

    name = fields.Char(string="Нэр", required=True)
    color = fields.Integer(string="Color")