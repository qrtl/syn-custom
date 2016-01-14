# -*- coding: utf-8 -*-
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2016 Rooms For (Hong Kong) Limited T/A OSCG
#    <https://www.odoo-asia.com>
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

from openerp.osv import fields, osv

class mail_mail(osv.Model):
    _inherit = "mail.mail"

    def send_get_mail_subject(self, cr, uid, mail, force=False, partner=None, context=None):
        """If subject is void, set the subject as '[odoo] <Resource>' or
        '[odoo] Re: <mail.parent_id.subject>'

            :param boolean force: force the subject replacement
        """
        if (force or not mail.subject) and mail.record_name:
            return '[odoo] %s' % (mail.record_name)
        elif (force or not mail.subject) and mail.parent_id and mail.parent_id.subject:
            return '[odoo] Re: %s' % (mail.parent_id.subject)
        return mail.subject

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
