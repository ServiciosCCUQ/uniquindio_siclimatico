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

            if not entrada:
                _logger.info('Input Vacio')
                return False

            # Fix - comillas dobles
            # entrada_raw = entrada.replace('"', "'")
            # _logger.info('entrada_raw %s', entrada_raw)

            json_clima = json.loads(entrada)

            _logger.info('json_clima = %s', json_clima)
            _logger.info('type json_clima = %s', type(json_clima))

            dir_viento = json_clima.get('dir')

            _logger.info('dir_viento %s', dir_viento)

            # for info in info_sensores:
            #    mediciones_model.create(info)

        except Exception as e:
            _logger.info('Error General = %s ', e)
        except ValueError as e:
            _logger.info('Error leyendo json %s', e)
