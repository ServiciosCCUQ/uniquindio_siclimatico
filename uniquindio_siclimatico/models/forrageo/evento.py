# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-
from datetime import datetime, timedelta
import logging
from openerp import models, fields, api

ESTADOS = [
    ('nuevo', 'Nuevo'),
    ('aprobado', u'Revisado'),
    ('anulado', u'Descartado'),
]

LIB = [
    ('noa', 'No Asociado'),
    ('rev', u'Revisado'),
    ('aso', u'Asociado'),
]

_logger = logging.getLogger(__name__)


class Evento(models.Model):
    _name = 'uniquindio.fr.evento'
    _order = 'fecha'

    especies = fields.Integer('No. Individuos', required=False)
    fecha = fields.Datetime(u'Fecha Evento', index=True)
    notas = fields.Text('Notas', required=False)
    foto_name = fields.Char('Nombre Archivo')
    foto = fields.Binary('Fotografia')
    especie_ids = fields.One2many(
        string='Especies', comodel_name='uniquindio.fr.evento.especie',
        inverse_name='evento_id', required=False)
    state = fields.Selection(ESTADOS, 'Estado', default="nuevo", index=True)
    state_libacion = fields.Selection(
        LIB, 'Estado Libacion', default="noa", index=True)

    @api.multi
    def bt_revisar(self):
        self.write({'state': 'aprobado'})

    @api.multi
    def bt_anular(self):
        self.write({'state': 'anulado'})

    @api.multi
    def bt_reopen(self):
        self.write({'state': 'nuevo'})

    @api.multi
    def bt_revisar_especie(self):
        especie = self.env.context.get('especie')
        genero = self.env.context.get('genero')

        especie_obj = self.env['uniquindio.fr.especie']
        especie_id = especie_obj.search(
            [('codinterno', '=', especie)], limit=1)

        genero_id = especie_id.genero_id
        familia_id = genero_id.familia_id

        vals = {'genero': genero, 'especie_id': especie_id.id,
                'genero_id': genero_id.id, 'familia_id': familia_id.id}
        self.write({'especie_ids': [(0, 0, vals)], 'state': 'aprobado'})

        return True

    def get_fechas(self, fecha_raw):
        """ obt fechas de busqueda de Libacion de acuerdo info de captura"""
        f_evento = datetime.strptime(fecha_raw, "%Y-%m-%d %H:%M:%S")
        f_ajuste = f_evento - timedelta(seconds=3)

        f_inicio = f_evento.strftime("%Y-%m-%d %H:%M:%S")
        f_fin = f_ajuste.strftime("%Y-%m-%d %H:%M:%S")

        return f_fin, f_inicio

    @api.multi
    def bt_asociar_libacion(self):
        libacion_obj = self.env['uniquindio.fr.libacion']
        dominio_busqueda = [('state_libacion', 'in', ['noa', 'rev'])]
        eventos_ids = self.search(dominio_busqueda)

        for eve in eventos_ids:
            f_inicio, f_fin = self.get_fechas(eve.fecha)
            dominio_libacion = [
                ('fecha', '>=', f_inicio), ('fecha', '<=', f_fin),
                ('state', '=', 'noconfir')]

            libacion_ids = libacion_obj.search(
                dominio_libacion, order="fecha desc", limit=1)

            if libacion_ids:
                # _logger.info('domain %s = ', dominio_libacion)
                # _logger.info('Evento id = %s |', eve.id)
                # _logger.info('Libaciones id = %s  |', libacion_ids.ids)
                vals = {'evento_id': eve.id, 'state': 'confir'}
                libacion_ids.write(vals)
                eve.state_libacion = 'aso'
            else:
                eve.state_libacion = 'rev'
