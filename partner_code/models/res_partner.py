# -*- coding: utf-8 -*-
from odoo import api, fields, models , _
from odoo.exceptions import ValidationError


class Partner(models.Model):
    _inherit = 'res.partner'

    code = fields.Char(size=64, index=True, tracking=True)

    @api.constrains('code')
    def _check_barcode_unicity(self):
        if self.env['res.partner'].search_count([('code', '=', self.code)]) > 1:
            raise ValidationError('An other user already has this code')

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if name:
            args = ['|', '|', '|', ('name', operator, name), ('code', operator, name),
                    ('mobile', operator, name), ('email', operator, name)] + args
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)

    @api.model
    def create(self, values):
        if not values['code']:
            values['code'] = self.env['ir.sequence'].with_company(values.get('company_id')).next_by_code(
                'res.partner') or 'New'

        return super(Partner, self).create(values)
