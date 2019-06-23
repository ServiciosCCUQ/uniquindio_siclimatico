# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-
from openerp import models, fields


class Libacion(models.Model):
    _name = 'uniquindio.fr.libacion'

    flor = fields.Integer('No. Flor', required=True)
    notas = fields.Text('Notas', required=False)
