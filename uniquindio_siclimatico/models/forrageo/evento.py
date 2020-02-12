# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-
from openerp import models, fields, api

ESTADOS = [
    ('nuevo', 'Nuevo'),
    ('aprobado', u'Revisado'),
    ('anulado', u'Descartado'),
]


class Evento(models.Model):
    _name = 'uniquindio.fr.evento'

    especies = fields.Integer('No. Individuos', required=False)
    fecha = fields.Datetime(u'Fecha Evento')
    notas = fields.Text('Notas', required=False)
    foto_name = fields.Char('Nombre Archivo')
    foto = fields.Binary('Fotografia')
    especie_ids = fields.One2many(
        string='Especies', comodel_name='uniquindio.fr.evento.especie',
        inverse_name='evento_id', required=False)
    state = fields.Selection(ESTADOS, 'Estado', default="nuevo")

    @api.multi
    def bt_revisar(self):
        self.write({'state': 'aprobado'})

    @api.multi
    def bt_anular(self):
        self.write({'state': 'anulado'})

    @api.multi
    def bt_reopen(self):
        self.write({'state': 'nuevo'})

    @api.multi
    def bt_revisar_especie(self, especie):
        pass
