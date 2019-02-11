# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-
from openerp import models, fields

estados = [
    (1, 'Activa'),
    (2, u'Desactivada'),
]


class Estacion(models.Model):
    _name = 'uniquindio.estacion'

    name = fields.Char('Nombre', required=True)
    codinterno = fields.Char('Codigo Interno',)
    coordenadax = fields.Char('Coordenas en X', required=False)
    coordenaday = fields.Char('Coordenas en Y', required=False)
    state = fields.Selection(
        string='Estado', required=True,  selection=estados, default=1)
    descripcion = fields.Text(u'Descripción', required=False)
    sensores_ids = fields.One2many(
        string='Sensores', comodel_name='uniquindio.estacion.sensores',
        inverse_name='estacion_id')
