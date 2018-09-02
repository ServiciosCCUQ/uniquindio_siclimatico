# -*- encoding: utf-8 -*-
from openerp import models,fields

estados = [
	(1, 'Activa'),
	(2, u'Desactivada'),
]

class Estacion(models.Model):
	_name='uniquindio.estacion'
	
	name = fields.Char('Nombre', required=True)
	codinterno = fields.Char('Codigo Interno',)
	coordenadax = fields.Text('Coordenas en X', required=False)
	coordenaday = fields.Text('Coordenas en Y', required=False)
	state = fields.Selection(string='Estado', required=True,  selection=estados )
	descripcion = fields.Text('Descripcion', required=False)
	sensores_ids = fields.One2many(string='Sensores',comodel_name='uniquindio.estacion.sensores',inverse_name='estacion_id')

