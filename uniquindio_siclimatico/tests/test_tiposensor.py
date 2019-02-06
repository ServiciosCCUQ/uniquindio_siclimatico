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
from openerp.exceptions import AccessError

_logger = logging.getLogger(__name__)


class TestTipoSensor(TransactionCase):

    def setUp(self):
        super(TestTipoSensor, self).setUp()
        self.model = self.env['uniquindio.tiposensor']
        self.user_model = self.env['res.users']
        self.main_company = self.env.ref('base.main_company')
        partner_manager = self.env.ref('base.group_partner_manager')
        self.csp_admin = self.env.ref('uniquindio_siclimatico.csp_admin')
        self.csp_inve = self.env.ref('uniquindio_siclimatico.csp_investigador')
        self.csp_estacion = self.env.ref('uniquindio_siclimatico.csp_estacion')

        # No enviar confirmacion para el reinicio de clave
        contex = {'no_reset_password': True}

        self.admin_user = self.user_model.with_context(contex).create(dict(
            name="Administrador",
            company_id=self.main_company.id,
            login="soporte1",
            email="soporte1@ceam-csp.me",
            color=1,
            function='Friend',
            date='2015-03-28',
            groups_id=[(6, 0, [self.csp_admin.id, partner_manager.id])]
        ))
        self.inv_user = self.user_model.with_context(contex).create(dict(
            name="Investigador",
            company_id=self.main_company.id,
            login="inv1",
            email="invt1@ceam-csp.me",
            # notify_email='none',
            groups_id=[(6, 0, [self.csp_inve.id, partner_manager.id])]
        ))
        self.est_user = self.user_model.with_context(contex).create(dict(
            name="Estacion",
            company_id=self.main_company.id,
            login="est1",
            email="est1@ceam-csp.me",
            # notify_email='none',
            groups_id=[(6, 0, [self.csp_estacion.id, partner_manager.id])]
        ))

        self.tiposensor = self.model.create(
            dict(name="Humedad-Sensor", tipo=2, unidad='%'))

    def test_crear(self):

        # Validar que SI se pueda crear con el usuario administrador
        usr = self.admin_user.id
        self.tiposensor1 = self.model.sudo(usr).create(
            dict(name="Humedad-Y69", tipo=2, unidad='%'))

        # No permitir crear sensores de parte de un Investigador
        with self.assertRaises(AccessError):
            usr = self.inv_user.id
            self.tiposensor2 = self.model.sudo(usr).create(
                dict(name="Temperatura DHT11",
                     tipo=1,
                     unidad='Grados Centigrados'))

        # No permitir crear sensores de parte de una estacion
        with self.assertRaises(AccessError):
            usr = self.est_user.id
            self.tiposensor3 = self.model.sudo(usr).create(
                dict(name="Temperatura DHT11",
                     tipo=1,
                     unidad='Grados Centigrados'))

    def test_modificar(self):
        nombre_sensor = 'sensor humedad'

        usr = self.admin_user.id
        self.tiposensor.sudo(usr).write({'name': nombre_sensor})
        self.assertEqual(self.tiposensor.name, nombre_sensor)

        # No permitir crear sensores de parte de un Investigador
        with self.assertRaises(AccessError):
            usr = self.inv_user.id
            self.tiposensor.sudo(usr).write({'name': nombre_sensor})

        # No permitir crear sensores de parte de una estacion
        with self.assertRaises(AccessError):
            usr = self.est_user.id
            self.tiposensor.sudo(usr).write({'name': nombre_sensor})

    def test_consultar(self):

        usr = self.admin_user.id
        estaciones_ids = self.model.sudo(usr).search([])
        self.assertNotEqual(len(estaciones_ids), 0)

        usr = self.inv_user.id
        estaciones_ids = self.model.sudo(usr).search([])
        self.assertNotEqual(len(estaciones_ids), 0)

        usr = self.est_user.id
        estaciones_ids = self.model.sudo(usr).search([])
        self.assertNotEqual(len(estaciones_ids), 0)

    def test_eliminar(self):

        usr = self.admin_user.id
        with self.assertRaises(AccessError):
            self.tiposensor.sudo(usr).unlink()

        with self.assertRaises(AccessError):
            usr = self.inv_user.id
            self.tiposensor.sudo(usr).unlink()

        with self.assertRaises(AccessError):
            usr = self.est_user.id
            self.tiposensor.sudo(usr).unlink()
