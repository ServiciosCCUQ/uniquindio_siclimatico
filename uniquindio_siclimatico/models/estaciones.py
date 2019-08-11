# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-
import logging
import urllib2
import json
from openerp import models, fields, api

estados = [
    (1, 'Activa'),
    (2, u'Desactivada'),
]

_logger = logging.getLogger(__name__)


class Estacion(models.Model):
    _name = 'uniquindio.estacion'

    name = fields.Char('Nombre', required=True)
    codinterno = fields.Char('Codigo Interno',)
    coordenadax = fields.Char('Latitud', required=False)
    coordenaday = fields.Char('Longitud', required=False)
    state = fields.Selection(
        string='Estado', required=True,  selection=estados, default=1)
    descripcion = fields.Text(u'Descripción', required=False)
    sensores_ids = fields.One2many(
        string='Sensores', comodel_name='uniquindio.estacion.sensores',
        inverse_name='estacion_id')

    _sql_constraints = [('estacion_unique', 'unique(name,codinterno)',
                         'La estacion ya existe.')]

    @api.multi
    def openweather_api(self):
        # https://openweathermap.org/api

        estacion = self.search([('codinterno', '=', 'openweathermap')])

        if not estacion:
            _logger.info('No se encontro estacion [OpenWeather]')
            return False

        estacion = estacion[0]

        token = '939b6911af0d21e35318d73aa8c3cfd0'
        lat = estacion.coordenadax  # '4.608512'
        lon = estacion.coordenaday  # '-75.723542'

        url_base = "http://api.openweathermap.org/data/2.5/weather?" \
                   "lat=%s&lon=%s&appid=%s&units=metric&lang=es"
        url = url_base % (lat, lon, token)

        _logger.info('Consumo de URL %s \n', url)

        req = urllib2.urlopen(url)
        data = req.read()

        json_data = json.loads(data.decode('utf-8'))

        if json_data:
            # json_data = eval(json_data)
            _logger.info('clima %s \n', json_data)
            mediciones_model = self.env['uniquindio.medicion']
            info_sensores = []

            # descripcion del clima: Nublado / Lluvioso
            # estado = json_data.get('weather')[0]['description']
            vel_viento = json_data.get('wind')['speed']

            # Aveces no llega el valor de grados en el viento ...
            if 'deg' in json_data.get('wind'):
                dir_viento = json_data.get('wind')['deg']
                info_sensores.append(self.diccionario(
                    estacion.id, 'dir_viento_generic', dir_viento))

            humedad = json_data.get('main')['humidity']
            pres_adm = json_data.get('main')['pressure']
            temp = json_data.get('main')['temp']

            info_sensores.append(self.diccionario(
                estacion.id, 'vel_viento_generic', vel_viento))
            info_sensores.append(self.diccionario(
                estacion.id, 'humedad_generic', humedad))
            info_sensores.append(self.diccionario(
                estacion.id, 'p_admosferica_generic', pres_adm))
            info_sensores.append(self.diccionario(
                estacion.id, 'temp_generic', temp))

            for info in info_sensores:
                mediciones_model.create(info)

            return True

    @api.multi
    def darksky_api(self):
        # https://darksky.net/dev/docs

        estacion = self.search([('codinterno', '=', 'darksky')])

        if not estacion:
            _logger.info('No se encontro estacion [darksky]')
            return False

        estacion = estacion[0]

        token = '1a74d395b7d78e6ae39f9803c054701a'

        lat = estacion.coordenadax  # '4.608512'
        lon = estacion.coordenaday  # '-75.723542'

        url_base = "https://api.darksky.net/forecast/%s/%s,%s?" \
                   "lang=es&units=si"
        url = url_base % (token, lat, lon)

        _logger.info('Consumo de URL %s \n', url)

        req = urllib2.urlopen(url)
        data = req.read()

        json_data = json.loads(data.decode('utf-8'))

        if json_data:
            # json_data = eval(json_data)
            # _logger.info('clima %s \n',json_data)
            mediciones_model = self.env['uniquindio.medicion']

            # descripcion del clima: Nublado / Lluvioso
            # estado = json_data.get('currently')['summary']
            vel_viento = json_data.get('currently')['windSpeed']
            dir_viento = json_data.get('currently')['windGust']
            humedad = json_data.get('currently')['humidity']
            pres_adm = json_data.get('currently')['pressure']
            temp = json_data.get('currently')['temperature']

            lluvia = json_data.get('currently')['precipIntensity']
            ozono = json_data.get('currently')['ozone']
            uvindex = json_data.get('currently')['uvIndex']

            info_sensores = []

            info_sensores.append(self.diccionario(
                estacion.id, 'vel_viento_generic', vel_viento))
            info_sensores.append(self.diccionario(
                estacion.id, 'dir_viento_generic', dir_viento))
            info_sensores.append(self.diccionario(
                estacion.id, 'humedad_generic', (humedad * 100)))
            info_sensores.append(self.diccionario(
                estacion.id, 'p_admosferica_generic', pres_adm))
            info_sensores.append(self.diccionario(
                estacion.id, 'temp_generic', temp))

            info_sensores.append(self.diccionario(
                estacion.id, 'precipitaciones_generic', lluvia))
            info_sensores.append(self.diccionario(
                estacion.id, 'ozono_generic', ozono))
            info_sensores.append(self.diccionario(
                estacion.id, 'uv_generic', uvindex))

            for info in info_sensores:
                mediciones_model.create(info)

            return True

    @api.model
    def comprobar_ws_clima(self):
        self.openweather_api()
        self.darksky_api()

    @api.multi
    def tipo_sensor(self, codinterno):
        sensor_id = self.env['uniquindio.tiposensor'].search(
            [('codinterno', '=', codinterno)])
        return sensor_id

    @api.multi
    def diccionario(self, estacion_id, tipo, valor, fecha=None):
        if not fecha:
            fecha = fields.datetime.now()
        tipo_id = self.tipo_sensor(tipo).id
        unidad = self.tipo_sensor(tipo).unidad
        vals = {'estacion_id': estacion_id, 'tipo_id': tipo_id,
                'valor': valor, 'unidad':  unidad, 'fecha': fecha}
        return vals
