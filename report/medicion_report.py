# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-


from openerp import tools
from openerp import models, fields, api

class MedicionReport(models.Model):
	_name = "uniquindio.medicion.report"
	_description = "Medicion - Report"
	_auto = False

	f_creacion = fields.Date(string='Fecha Creacion', readonly=True)
	dia = fields.Char(string='Dia', readonly=True)
	mes = fields.Char(string='Mes', readonly=True)
	anio = fields.Char(string=u'Año', readonly=True)
	avg = fields.Float(string='Promedio', readonly=True)
	maximo = fields.Float(string='Maximo', readonly=True)
	minimo = fields.Float(string='Minimo', readonly=True)
	tipo_id = fields.Many2one(string='Tipo',required=True,comodel_name='uniquindio.tiposensor')
	estacion_id = fields.Many2one(string='Estacion',required=True,comodel_name='uniquindio.estacion')


	def init(self, cr):
		tools.drop_view_if_exists(cr, self._table)
		cr.execute("""CREATE or REPLACE VIEW %s as (
			SELECT  
				row_number() OVER() AS id, 
				m.create_date::date as "f_creacion", 
				date_part('day', m.create_date)::text as dia , 
				date_part('month', m.create_date)::text as mes , 
				date_part('year', m.create_date)::text as anio ,  
				avg(m.valor), 
				max(m.valor) as "maximo",
				min(m.valor) as "minimo" , 
				tipo_id , 
				estacion_id 
			FROM 
			uniquindio_medicion m 
			GROUP BY 
			tipo_id , estacion_id ,m.create_date::date , date_part('month', create_date) , date_part('day', create_date) , date_part('year', create_date) 									
		)""" % (
					self._table
				)
		)
