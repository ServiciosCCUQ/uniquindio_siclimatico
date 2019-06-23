# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-
from openerp import models, fields


class Libacion(models.Model):
    _name = 'uniquindio.fr.evento'

    especies = fields.Integer('No. Individuos', required=False)
    notas = fields.Text('Notas', required=False)
    foto_name = fields.Char('Nombre Archivo')
    foto = fields.Binary('Fotografia')
    especie_ids = fields.One2many(
        string='Especies', comodel_name='uniquindio.fr.evento.especie',
        inverse_name='evento_id', required=False)
