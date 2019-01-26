# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2018 Gustavo Salgado
#    @author Gustavo Salgado Ocampo <gasalgadoo@uqvirtual.edu.co>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import logging
from openerp.tests.common import TransactionCase

_logger = logging.getLogger(__name__)


class TestTipoSensor(TransactionCase):

    def setUp(self):
        super(TestTipoSensor, self).setUp()
        self.saludo = 'Primera Prueba Odoo'
        _logger.info('[setUp] esto es una impresion desde pruebas unitarias.')
        _logger.info(self.saludo)

    def prueba1(self):
        _logger.info('[prueba1] pruebas unitarias...')
        _logger.info(self.saludo)
        self.assertEqual(self.saludo, 'Primera Prueba Odoo')
