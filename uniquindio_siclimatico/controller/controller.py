# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-
import logging
from openerp.addons.web import http

_logger = logging.getLogger(__name__)


class Arduino(http.Controller):

    @http.route('/api/dost/', type='http', auth='none', cors='*')
    def ping(self, **kw):
        _logger.info('Hola!')
        # Play with stuff, E.g:
        # env = http.request.env
        # werkzeug_request = http.request.httprequest
        # werkzeug_request.get_data()
        # str_data = werkzeug_request.data
        # and other parameters, please read Odoo document
        return "ok"
