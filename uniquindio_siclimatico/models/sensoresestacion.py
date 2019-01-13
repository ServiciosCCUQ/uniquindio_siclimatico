# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-
from openerp import models, fields

estados = [
    (1, 'Activo'),
    (2, u'Descalibrado'),
    (3, 'Desactivado'),
    (4, u'Fuera de Linea'),
]


class SensoresEstacion(models.Model):
    _name = 'uniquindio.estacion.sensores'

    estacion_id = fields.Many2one(
        string='Estacion', required=True, comodel_name='uniquindio.estacion')
    tipo_id = fields.Many2one(
        string='Tipo', required=True, comodel_name='uniquindio.tiposensor')
    intervalo = fields.Integer('Intervalo Medicion(Minutos)', required=True)
    state = fields.Selection(
        string='Estado', required=True,  selection=estados)
