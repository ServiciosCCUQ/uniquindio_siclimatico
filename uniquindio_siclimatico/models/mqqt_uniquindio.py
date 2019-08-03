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

            estacion = self.search([('codinterno', '=', 'ladivisa')])

            if not estacion:
                _logger.info('No se encontro estacion [ladivisa]')
                return False

            estacion = estacion[0]

            # mediciones_model = self.env['uniquindio.medicion']

            info_sensores = []

            dir_viento = json_clima.get('dir')
            # vel1_viento = json_clima.get('speed1')
            # vel5_viento = json_clima.get('speed5')
            # lluvia1 = json_clima.get('hour1')
            # lluvia24 = json_clima.get('hour24')
            # temp = json_clima.get('temp')
            # hum = json_clima.get('hum')
            # pres_adm = json_clima.get('bp')
            # co2 = json_clima.get('co2')
            # voc = json_clima.get('voc')

            info_sensores.append(estacion.diccionario(
                estacion.id, 'dir_viento_generic', dir_viento))

        except Exception as e:
            _logger.info('json invalido = %s ', e)