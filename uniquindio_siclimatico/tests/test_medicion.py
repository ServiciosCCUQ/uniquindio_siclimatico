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


class Testmedicion(TransactionCase):

    def setUp(self):
        super(Testmedicion, self).setUp()
        self.model = self.env['uniquindio.medicion']
        self.model_ts = self.env['uniquindio.tiposensor']
        self.model_e = self.env['uniquindio.estacion']
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
            groups_id=[(6, 0, [self.csp_inve.id, partner_manager.id])]
        ))
        self.est_user = self.user_model.with_context(contex).create(dict(
            name="Estacion",
            company_id=self.main_company.id,
            login="est1",
            email="est1@ceam-csp.me",
            groups_id=[(6, 0, [self.csp_estacion.id, partner_manager.id])]
        ))

        self.ts = self.model_ts.create(
            dict(name="Humedad-Sensor", tipo=2, unidad='%'))

        self.e = self.model_e.create(
            dict(name="BlueStation", state=1, codinterno='blue'))

        estacion = self.e.id
        tipo = self.ts.id

        self.medicion = self.model.create(
            dict(estacion_id=estacion, tipo_id=tipo, valor=10, unidad='%'))

    def test_crear(self):

        estacion = self.e.id
        tipo = self.ts.id

        # Validar que SI se pueda crear con el usuario Estacion
        usr = self.est_user.id
        self.medicion1 = self.model.sudo(usr).create(
            dict(estacion_id=estacion, tipo_id=tipo, valor=20, unidad='%'))

        # No permitir crear sensores de parte de un Investigador
        with self.assertRaises(AccessError):
            usr = self.inv_user.id
            self.medicion2 = self.model.sudo(usr).create(
                dict(estacion_id=estacion, tipo_id=tipo, valor=22, unidad='%'))

        # No permitir crear sensores de parte de una Administrador
        with self.assertRaises(AccessError):
            usr = self.admin_user.id
            self.medicion3 = self.model.sudo(usr).create(
                dict(estacion_id=estacion, tipo_id=tipo, valor=25, unidad='%'))

    def test_modificar(self):
        valor = 21
        usr = self.est_user.id
        self.medicion.sudo(usr).write({'valor': valor})
        self.assertEqual(self.medicion.valor, valor)

        # No permitir crear sensores de parte de un Investigador
        with self.assertRaises(AccessError):
            usr = self.inv_user.id
            self.medicion.sudo(usr).write({'valor': valor})

        # No permitir crear sensores de parte de Administrador
        with self.assertRaises(AccessError):
            usr = self.admin_user.id
            self.medicion.sudo(usr).write({'valor': valor})

    def test_consultar(self):

        usr = self.admin_user.id
        mediciones_ids = self.model.sudo(usr).search([])
        self.assertNotEqual(len(mediciones_ids), 0)

        usr = self.inv_user.id
        mediciones_ids = self.model.sudo(usr).search([])
        self.assertNotEqual(len(mediciones_ids), 0)

        usr = self.est_user.id
        mediciones_ids = self.model.sudo(usr).search([])
        self.assertNotEqual(len(mediciones_ids), 0)

    def test_eliminar(self):

        usr = self.admin_user.id
        with self.assertRaises(AccessError):
            self.medicion.sudo(usr).unlink()

        with self.assertRaises(AccessError):
            usr = self.inv_user.id
            self.medicion.sudo(usr).unlink()

        with self.assertRaises(AccessError):
            usr = self.est_user.id
            self.medicion.sudo(usr).unlink()
