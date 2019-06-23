# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-
from openerp import models, fields

tipos = [
    (1, 'Temperatura'),
    (2, u'Humedad'),
    (3, 'Velocidad del Viento'),
    (4, u'Radiación UltraVioleta'),
    (5, u'Precipitación'),
    (6, u'CO2'),
    (7, u'Presión Admosferica'),
    (8, u'Dirección del Viento'),
    (9, u'Ozono'),
]


class TipoSensor(models.Model):
    _name = 'uniquindio.tiposensor'

    name = fields.Char('Nombre Sensor', required=True)
    codinterno = fields.Char('Nombre Interno')
    tipo = fields.Selection(string='Tipo', required=True,  selection=tipos)
    descripcion = fields.Text('Descripcion', required=False)
    unidad = fields.Char('Unidad de Medica', required=True)

    _sql_constraints = [('tiposensor_unique', 'unique(name,tipo)',
                         'Ya existe un tipo sensor con este nombre.')]
