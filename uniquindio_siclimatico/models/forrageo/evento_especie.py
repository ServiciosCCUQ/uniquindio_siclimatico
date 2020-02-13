# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-
from openerp import models, fields, api

gen = [
    ('m', 'Macho'),
    ('h', u'Hembra'),
    ('i', u'Indeterminado'),
]


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
    individuos = fields.Integer('# Individos', required=True, default=1)
    genero = fields.Selection(string=u'Género', required=True, selection=gen)
    notas = fields.Text('Notas', required=False)

    @api.onchange('especie_id')
    def on_especie_id(self):
        if self.especie_id:
            self.genero_id = self.especie_id.genero_id.id
            self.familia_id = self.genero_id.familia_id.id
