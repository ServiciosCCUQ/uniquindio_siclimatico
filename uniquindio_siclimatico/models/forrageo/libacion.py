# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-
from openerp import models, fields

ESTADOS = [
    ('noconfir', 'Sin Confirmar'),
    ('confir', u'Confirmada'),
    ('anulada', u'Anulada'),
]


class Libacion(models.Model):
    _name = 'uniquindio.fr.libacion'
    _order = 'fecha'

    flor = fields.Integer('No. Flor', required=True)
    fecha = fields.Datetime(u'Fecha Libación', index=True)
    notas = fields.Text('Notas', required=False)
    state = fields.Selection(
        ESTADOS, 'Estado', default="noconfir", index=True)
    evento_id = fields.Many2one(
        string='Evento', required=True,
        comodel_name='uniquindio.fr.evento', index=True)
