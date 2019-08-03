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

    @api.multi
    def recibir_clima(self, entrada):
        try:
            json_clima = json.loads(entrada.decode('utf-8'))

            if not json_clima:
                _logger.info('Json esta vacio!')
                return False

            estacion_model = self.env['uniquindio.estacion']
            busqueda_estacion = [('codinterno', '=', 'ladivisa')]
            estacion = estacion_model.search(busqueda_estacion)

            if not estacion:
                _logger.info('No se encontro estacion [ladivisa]')
                return False

            estacion = estacion[0]

            mediciones_model = self.env['uniquindio.medicion']

            info_sensores = []

            # fecha = json_clima.get('fecha')
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

            _logger.info('dir_viento %s', dir_viento)
            _logger.info('vel1_viento %s', vel1_viento)
            _logger.info('vel5_viento %s', vel5_viento)
            _logger.info('lluvia1 %s', lluvia1)
            _logger.info('lluvia24 %s', lluvia24)
            _logger.info('temp %s', temp)
            _logger.info('hum %s', hum)
            _logger.info('pres_adm %s', pres_adm)
            _logger.info('co2 %s', co2)
            _logger.info('voc %s', voc)

            _logger.info('Data persistir %s', info_sensores)
            _logger.info('mediciones_modelo %s', mediciones_model)

            # for info in info_sensores:
            #    mediciones_model.create(info)

        except Exception as e:
            _logger.info('Error General = %s ', e)
        except ValueError as e:
            _logger.info('Error leyendo json %s', e)
