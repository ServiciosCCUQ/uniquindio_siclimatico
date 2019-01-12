# -*- encoding: utf-8 -*-
from openerp import models,fields

class Medicion(models.Model):
	_name='uniquindio.medicion'

	estacion_id = fields.Many2one(string='Estacion',required=True,comodel_name='uniquindio.estacion',index=True)
	tipo_id = fields.Many2one(string='Tipo',required=True,comodel_name='uniquindio.tiposensor',index=True)	
	valor = fields.Float('Valor', required=True , group_operator="avg",index=True)
	unidad = fields.Char('Unidad Medida', required=True,index=True)

