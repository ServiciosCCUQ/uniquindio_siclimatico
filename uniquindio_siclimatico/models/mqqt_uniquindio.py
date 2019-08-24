# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-
##############################################################################
#
#    Universidad del Quindio
#    Proyecto para Semillero de Investigacion Fase III - 2019
#    Gustavo Salgado Ocampo - Fredy Alexander Espana
#
# This models is taken from Tectronix Spa module 'Mqtt Abstract Interface'
# https://apps.odoo.com/apps/modules/11.0/mqtt_abstract_interface/
#
##############################################################################
from datetime import datetime, timedelta
import logging
import json
# from openerp import models, fields , api
from openerp import models, api

# from openerp.modules.registry import Registry

_logger = logging.getLogger(__name__)


class Mqqt(models.Model):
    _name = 'uniquindio.mqqt'
    _inherit = 'iot.mqtt'

    @api.multi
    def on_message(self, client, userdata, msg):
        _logger.info('msg.topic %s ', msg.topic)
        _logger.info('msg.payload %s ', msg.payload)
        if msg.topic == 'clima':
            self.recibir_clima(msg.payload)
        if msg.topoc == 'libacion':
            self.recibir_libacion(msg.payload)

    @api.multi
    def recibir_libacion(self, entrada):
        with api.Environment.manage():
            new_cr = self.pool.cursor()
            self = self.with_env(self.env(cr=new_cr))
            try:
                if not entrada:
                    _logger.info('[Clima] Input Vacio')
                    return False

                json_libacion = json.loads(entrada)
                flor = json_libacion.get('flor')
                fecha = json_libacion.get('fecha')
                fecha = datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S")
                f = fecha.strftime("%Y-%m-%d %H:%M:%S")

                libacion_model = self.env['uniquindio.fr.libacion']
                vals = {'flor': flor, 'fecha': f}
                libacion_model.create(vals)

                new_cr.commit()
                new_cr.close()
            except Exception as e:
                self._cr.rollback()
                self._cr.close()
                _logger.info('Error General Libaciones = %s ', e)
            except ValueError as e:
                self._cr.rollback()
                self._cr.close()
                _logger.info('Error leyendo json Libacion %s', e)

    @api.multi
    def recibir_clima(self, entrada):
        with api.Environment.manage():
            new_cr = self.pool.cursor()
            self = self.with_env(self.env(cr=new_cr))

            try:
                if not entrada:
                    _logger.info('[Clima] Input Vacio')
                    return False

                json_clima = json.loads(entrada)

                _logger.info('json_clima = %s', json_clima)
                _logger.info('type json_clima = %s', type(json_clima))

                if not json_clima:
                    _logger.info('Json esta vacio!')
                    return False

                estacion_model = self.env['uniquindio.estacion']
                busqueda = [('codinterno', '=', 'divisa')]
                estacion = estacion_model.search(busqueda)

                estacion = estacion[0]

                mediciones_model = self.env['uniquindio.medicion']

                info_sensores = []

                fecha_raw = json_clima.get('fecha')
                dir_viento = json_clima.get('dir')
                vel1_viento = json_clima.get('speed1')
                vel5_viento = json_clima.get('speed5')
                lluvia1 = json_clima.get('hour1')
                lluvia24 = json_clima.get('hour24')
                temp = json_clima.get('temp')
                hum = json_clima.get('hum')
                pres_adm = json_clima.get('bp')
                co2 = json_clima.get('co2') or ''
                voc = json_clima.get('voc') or ''

                # Fecha en formato de arduino: Sat Aug 24 07:03:35 2019
                fecha = datetime.strptime(fecha_raw, "%a %b %e %H:%M:%S %Y")
                # Ajuste a UTC
                fecha = fecha + timedelta(hours=5)
                f = fecha.strftime("%Y-%m-%d %H:%M:%S")

                _logger.info('Fecha de captura %s', fecha)

                info_sensores.append(estacion.diccionario(
                    estacion.id, 'dir_viento_generic', dir_viento, fecha=f))
                info_sensores.append(estacion.diccionario(
                    estacion.id, 'vel_viento_generic', vel1_viento, fecha=f))
                info_sensores.append(estacion.diccionario(
                    estacion.id, 'vel_viento_5', vel5_viento, fecha=f))
                info_sensores.append(estacion.diccionario(
                    estacion.id, 'precipitaciones_generic', lluvia1, fecha=f))
                info_sensores.append(estacion.diccionario(
                    estacion.id, 'precipitaciones_24', lluvia24, fecha=f))
                info_sensores.append(estacion.diccionario(
                    estacion.id, 'temp_generic', temp, fecha=f))
                info_sensores.append(estacion.diccionario(
                    estacion.id, 'humedad_generic', hum, fecha=f))
                info_sensores.append(estacion.diccionario(
                    estacion.id, 'p_admosferica_generic', pres_adm, fecha=f))

                if co2:
                    info_sensores.append(estacion.diccionario(
                        estacion.id, 'eco2', co2))
                if voc:
                    info_sensores.append(estacion.diccionario(
                        estacion.id, 'voc', voc))

                for info in info_sensores:
                    mediciones_model.create(info)

                new_cr.commit()
                new_cr.close()
            except Exception as e:
                self._cr.rollback()
                self._cr.close()
                _logger.info('Error General = %s ', e)
            except ValueError as e:
                self._cr.rollback()
                self._cr.close()
                _logger.info('Error leyendo json %s', e)
