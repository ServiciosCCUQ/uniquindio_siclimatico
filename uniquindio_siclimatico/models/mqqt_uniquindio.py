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
        _logger.info('Implementacion ....')
        _logger.info('client %s ', client)
        _logger.info('userdata %s ', userdata)
        _logger.info('msg.topic %s ', msg.topic)
        _logger.info('msg.payload %s ', msg.payload)
        if msg.topic == 'clima':
            self.recibir_clima(msg.payload)
        if msg.topoc == 'libacion':
            self.recibir_libacion(msg.payload)

    @api.multi
    def recibir_libacion(self, entrada):
        _logger.info('Recibir Lib %s', entrada)
        return True

    @api.multi
    def recibir_clima(self, entrada):
        with api.Environment.manage():
            new_cr = self.pool.cursor()
            self = self.with_env(self.env(cr=new_cr))

            try:
                if not entrada:
                    _logger.info('Input Vacio')
                    return False

                # Fix - comillas dobles
                # entrada_raw = entrada.replace('"', "'")
                # _logger.info('entrada_raw %s', entrada_raw)

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

                info_sensores.append(estacion.diccionario(
                    estacion.id, 'dir_viento_generic', dir_viento))
                info_sensores.append(estacion.diccionario(
                    estacion.id, 'vel_viento_generic', vel1_viento))
                info_sensores.append(estacion.diccionario(
                    estacion.id, 'vel_viento_5', vel5_viento))
                info_sensores.append(estacion.diccionario(
                    estacion.id, 'precipitaciones_generic', lluvia1))
                info_sensores.append(estacion.diccionario(
                    estacion.id, 'precipitaciones_24', lluvia24))
                info_sensores.append(estacion.diccionario(
                    estacion.id, 'temp_generic', temp))
                info_sensores.append(estacion.diccionario(
                    estacion.id, 'humedad_generic', hum))
                info_sensores.append(estacion.diccionario(
                    estacion.id, 'p_admosferica_generic', pres_adm))

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
