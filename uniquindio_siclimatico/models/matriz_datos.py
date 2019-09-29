# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-
from datetime import datetime, timedelta
from dateutil import rrule
from dateutil.rrule import rruleset
import logging
from openerp import models, fields, api

fuente = [
    ('sitio', 'Sitio'),
    ('zona', u'Zona'),
]

_logger = logging.getLogger(__name__)


class MatrizActividad(models.Model):
    _name = 'uniquindio.matriz_actividad'

    name = fields.Char('Rango Tiempo', required=True)
    fecha = fields.Date(u'Fecha')
    dia = fields.Integer('Dia')
    h_inicio = fields.Datetime('Hora de Inicio', required=True)
    h_fin = fields.Datetime('Hora de Fin', required=True)
    libaciones = fields.Integer('Libaciones')
    frecuencia_libaciones = fields.Float('Frecuencia Libaciones')

    def utc_5(self, fecha):
        return (fecha - timedelta(hours=5))

    def utc_0(self, fecha):
        return (fecha + timedelta(hours=5))

    def rango(self, inicio, fin):
        return "%s:00 - %s:00" % (inicio, fin)

    def obtener_estacion(self, estacion):
        estacion_model = self.env['uniquindio.estacion']
        busqueda_est = [('codinterno', '=', estacion)]
        estacion = estacion_model.search(busqueda_est)

        return estacion[0]

    def lista_dias(self, f_inicio, f_fin):
        patron_regla = 'RRULE:FREQ=DAILY'

        # generando regla de repeticion
        rule = rrule.rrulestr(patron_regla,dtstart=f_inicio)

        # usar conjunto de reglas
        rules = rruleset()
        rules.rrule(rule)

        res = rules.between(f_inicio, f_fin, inc=True)

        return res

    def calcular_dias(self, f_inicio, f_fin):

        primera_fecha = datetime.strptime(f_inicio, "%Y-%m-%d %H:%M:%S")
        ultima_fecha = datetime.strptime(f_fin, "%Y-%m-%d %H:%M:%S")

        # ajuste utc a utc-5(colombia) -> se requiere mejorar
        primera_fecha = primera_fecha - timedelta(hours=5)
        ultima_fecha = ultima_fecha - timedelta(hours=5)

        # ajuste a horas iniciales y finales
        primera_fecha = primera_fecha.replace(hour=0, minute=0, second=0)
        ultima_fecha = ultima_fecha.replace(hour=23, minute=59, second=59)

        #_logger.info('1.Primera Fecha %s', primera_fecha)
        #_logger.info('1.Ultima Fecha %s', ultima_fecha)

        return self.lista_dias(primera_fecha, ultima_fecha)        

    def obtener_libaciones(self,lib_ids,f_inicio,f_fin):
        'Retorna cantidad de libaciones entre 2 fechas especificas'
        # _logger.info('2. f_inicio %s - type %s', f_inicio, type(f_inicio))
        # _logger.info('2. f_fin %s - type %s', f_fin, type(f_fin))
        filtro = lambda l: l.fecha >= str(f_inicio) and l.fecha < str(f_fin)        
        libaciones_ids = lib_ids.filtered(filtro)
        return len(libaciones_ids)

    def obtener_libaciones_dia(self,lib_ids,f_inicio):
        'Obtener cantidad de libaciones de un dia completo'
        #pasar f_inicio a UTC-0
        f_inicio = f_inicio + timedelta(hours=5)
        f_fin = f_inicio + timedelta(hours=24)
        return self.obtener_libaciones(lib_ids,f_inicio,f_fin)

    def obtener_libaciones_hora(self,lib_ids,f_inicio,h_inicio,h_fin):
        'Obtener cantidad de libaciones un rango de horas determinado'
        
        #ajustar fecha a hora de busqueda
        f_inicio = f_inicio.replace(hour=h_inicio)
        f_fin = f_inicio.replace(hour=h_fin)

        #pasar fechas a UTC-0
        f_inicio = f_inicio + timedelta(hours=5)
        f_fin = f_fin + timedelta(hours=5)

        return self.obtener_libaciones(lib_ids,f_inicio,f_fin) , f_inicio , f_fin     


    @api.multi
    def bt_calcular(self):
        'Generar Matriz de Datos para analisis estadistico'
        _logger.info('Iniciando Calculos de Matriz')

        medicion_model = self.env['uniquindio.medicion']
        libaciones_model = self.env['uniquindio.fr.libacion']

        estacion = self.obtener_estacion(estacion='divisa')

        # TODO: Analizar la resta de 5 horas para el UTC
        horas = [(5,6), (6,7), (7,8), (8,9), (9,10), (10,11), (11,12), (12,13), 
        (13,14), (14,15), (15,16), (16,17), (17,18), (18,19),(19,20)]

        medicion_ids = medicion_model.search([('estacion_id','=',estacion.id)],order='fecha')
        primera_fecha = medicion_ids[0].fecha
        ultima_fecha = medicion_ids[ len(medicion_ids) - 1 ].fecha

        # obtener los dias que se verificaran datos(rango de fechas)
        dias = self.calcular_dias(primera_fecha, ultima_fecha)

        # obtener libaciones (todas) -> luego se filtran
        libaciones_ids = libaciones_model.search([])

        # identificador de dias muestreo
        dia_muestra = 1

        for d in dias:
            lib_totales = self.obtener_libaciones_dia(libaciones_ids,d)
            _logger.info('Libaciones Dia[%s] %s' , str(d), lib_totales)
            for h in horas:
                h_inicio = h[0]
                h_fin = h[1]
                lib_hora, f_inicio , f_fin = self.obtener_libaciones_hora(libaciones_ids, d, h_inicio, h_fin)

                frecuencia_hora = 0
                if lib_totales > 0:
                    frecuencia_hora = float(lib_hora)/float(lib_totales)

                vals = { 'name' : self.rango(h_inicio,h_fin),
                        'fecha' : self.utc_0(d).date(),
                        'dia' : dia_muestra,
                        'h_inicio' : f_inicio,
                        'h_fin' : f_fin,
                        'libaciones' : lib_hora,
                        'frecuencia_libaciones' : frecuencia_hora
                }

                #_logger.info('dato estadistico= %s \n',vals)

                self.create(vals)
            dia_muestra = dia_muestra + 1


        pass