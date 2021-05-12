# Copyright 2012-2021 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    phonecall_ids = fields.One2many(
        'crm.phonecall', 'partner_id', string='Phone Calls')
    phonecall_count = fields.Integer(
        compute='_compute_phonecall_count', string='Number of Phonecalls')

    @api.depends('phonecall_ids')
    def _compute_phonecall_count(self):
        rg_res = self.env['crm.phonecall'].read_group(
            [('partner_id', 'in', self.ids)],
            ['partner_id'], ['partner_id'])
        mapped_data = dict([(x['partner_id'][0], x['partner_id_count']) for x in rg_res])
        for partner in self:
            partner.phonecall_count = mapped_data.get(partner.id, 0)
