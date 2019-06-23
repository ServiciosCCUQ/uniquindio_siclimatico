# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-
from openerp import models, fields


class EventoEspecie(models.Model):
    _name = 'uniquindio.fr.evento.especie'

    evento_id = fields.Many2one(
        string='Evento', required=True,
        comodel_name='uniquindio.fr.evento', index=True)
    familia_id = fields.Many2one(
        string='Familia', required=True,
        comodel_name='uniquindio.fr.familia', index=True)
    genero_id = fields.Many2one(
        string='Genero', required=True,
        comodel_name='uniquindio.fr.genero', index=True)
    especie_id = fields.Many2one(
        string='Especie', required=True,
        comodel_name='uniquindio.fr.especie', index=True)
    individuos = fields.Integer('No. Individos', required=True)
    notas = fields.Text('Notas', required=False)
