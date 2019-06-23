# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-
from openerp import models, fields


class Familia(models.Model):
    _name = 'uniquindio.fr.familia'

    name = fields.Char('Nombre Familia', required=True)
    codinterno = fields.Char('Codigo Interno Familia', required=True)
    notas = fields.Text('Descripcion')


class Genero(models.Model):
    _name = 'uniquindio.fr.genero'

    name = fields.Char('Nombre Genero', required=True)
    codinterno = fields.Char('Codigo Interno Genero', required=True)
    familia_id = fields.Many2one(
        string='Familia', required=True,
        comodel_name='uniquindio.fr.familia', index=True)
    notas = fields.Text('Descripcion')


class Especie(models.Model):
    _name = 'uniquindio.fr.especie'

    name = fields.Char('Nombre Especie', required=True)
    codinterno = fields.Char('Codigo Interno Especie', required=True)
    genero_id = fields.Many2one(
        string='Genero', required=True,
        comodel_name='uniquindio.fr.genero', index=True)
    notas = fields.Text('Descripcion')
    foto_name = fields.Char('Nombre Archivo')
    foto = fields.Binary('Imagen Referencia')
