import os

from odoo import http
from odoo.addons.web.controllers import main
from odoo.tools.translate import _


class CustomLoginController(main.Home):
    @http.route("/web/login", type="http", auth="none")
    def web_login(self, *args, **kw):
        main.ensure_db()
        allow_odoo_login = os.getenv("ODOO_ALLOW_ODOO_LOGIN", False)
        response = super(CustomLoginController, self).web_login(*args, **kw)
        if http.request.httprequest.method == "POST" and not allow_odoo_login:
            response.qcontext['error'] = _("The Odoo login is disabled")
        response.qcontext['allow_odoo_login'] = allow_odoo_login
        return response
