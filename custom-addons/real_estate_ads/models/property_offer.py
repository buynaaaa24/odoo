from email.policy import default

from reportlab.graphics.transform import inverse

from odoo import  fields, models, api, _
from datetime import timedelta

from odoo.exceptions import ValidationError


class TransientOffer(models.TransientModel):
    _name = 'transient.model.offer'
    _description = 'Abstract offers'

    @api.autovacuum
    def _transient_vacuum(self):
        pass


    partner_email = fields.Char(string="Email")
    partner_phone = fields.Char(string="Утасны дугаар")

class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Зарагдах бүтээгдэхүүний саналууд'

    @api.depends('property_id','partner_id')
    def _compute_name(self):
        for rec in self:
            if rec.property_id and rec.partner_id:
                rec.name = f"{rec.property_id} - {rec.partner_id.name}"
            else:
                rec.name = False

    name = fields.Char(string="Тайлбар", compute =_compute_name)
    price = fields.Float(string="Үнэ")
    status = fields.Selection(
        [('хүлээж авсан', 'ХҮЛЭЭЖ АВСАН'), ('татгалзсан', 'ТАТГАЛЗСАН')],
        string="Төлөв")
    partner_id = fields.Many2one('res.partner', string="Хэрэглэгч")
    property_id = fields.Many2one('estate.property', string="Бүтээгдэхүүн")
    validity = fields.Integer(string="Validity", default=7)
    deadline = fields.Date(string="Dead Line", compute='_compute_deadline', inverse='_inverse_deadline')

    @api.model
    def _set_create_date(self):
        return fields.Date.today()

    creation_date = fields.Date(string="Creation Date", default =_set_create_date)

    @api.depends('validity', 'creation_date')
    def _compute_deadline(self):
        for rec in self:
            if rec.creation_date:
               rec.deadline = rec.creation_date + timedelta(days=rec.validity)
    def _inverse_deadline(self):
        for rec in self:
            if rec.deadline and rec.creation_date:
                rec.validity = (rec.deadline - rec.creation_date).days
            else:
                rec.validity = False

    @api.model_create_multi
    def create(self, vals):
        for rec in vals:
            if not rec.get('creation_date'):
                rec['creation_date'] = fields.Date.today()
        return super(PropertyOffer,self).create(vals)

    # @api.constrains('validity')
    # def _check_validity(self):
    #     for rec in self:
    #         if rec.deadline <= rec.creation_date:
    #             raise ValidationError(_("Deadline cannot be before creation date"))
    
    def action_accept_offer(self):
        if self.property_id:
            self._validate_accepted_offer()
            self.property_id.write({
                'selling_price':self.price,
                'state':'хүлээж авсан'
            })
        self.status = 'хүлээж авсан'

    def _validate_accepted_offer(self):
        offer_ids = self.env['estate.property.offer'].search([
            ('property_id', '=', self.property_id.id),
            ('status', '=', 'accepted'),
        ])
        if offer_ids:
            raise ValidationError("Аль хэдийн хүлээн зөвшөөрсөн байна")

    def action_decline_offer(self):
        self.status = 'татгалзсан'
        print(all(self.property_id.offer_ids.mapped('status')))
        if all(self.property_id.offer_ids.mapped('status')):
            self.property_id.write({
                'selling_price': 0,
                'state': 'received'
            })
#Abstract,Transient, Regular Model

    def extend_offer_deadline(self):
        active_ids = self._context.get('active_ids', [])
        if active_ids:
            offer_ids = self.env['estate.property.offer'].browse(active_ids)
            for offer in offer_ids:
                offer.validity = 10

    def _extend_offer_deadline(self):
        offer_ids = self.env['estate.property.offer'].search([])
        for offer in offer_ids:
            offer.validity = offer.validity + 1
