# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2012 OpenERP S.A (<http://www.openerp.com>).
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

{
    'name': 'Uniquindio: Sistema de Informacion Climatico',
    'version': '1.0',
    'depends': ['base'],
    'author': 'Gustavo Salgado - Fredy Alexander Espana',
    'website': 'https://www.odoo.com/',
    'category': 'iot',
    'description':
        """
    Sistema de Informacion Climatico

    Gestion de Datos Climaticos y Representación
    de Variables a traves de Analitica
    """,
        'data': [
            'security/uniquindio_siclimatico_security.xml',
            'security/ir.model.access.csv',
            'views/sic_menu.xml',
            'views/tiposensor_view.xml',
            'views/estaciones_view.xml',
            'views/medicion_view.xml',
            'report/medicion_report_view.xml',
    ],
    'auto_install': False,
    'installable': True,
}
