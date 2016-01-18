# -*- coding: utf-8 -*-
#    Odoo, Open Source Management Solution
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

{
    'name': 'Database Manager Menu Custom',
    'summary':"""""",
    'version': '8.0.0.5.0',
    'category': 'Hidden',
    'description': """
* Change the menu name of 'Drop' in Database Manager to '------------------Drop Database'
    """,
    'author': 'Rooms For (Hong Kong) Limited T/A OSCG',
    'website': 'https://www.odoo-asia.com',
    'license': 'AGPL-3',
    'depends': ['web',],
    'qweb' : [
        'static/src/xml/base.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
