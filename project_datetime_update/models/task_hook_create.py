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

from openerp import models
from openerp.addons.project.project import task


def create(self, cr, uid, vals, context=None):
    context = dict(context or {})

    # for default stage
    if vals.get('project_id') and not context.get('default_project_id'):
        context['default_project_id'] = vals.get('project_id')
    # >>> modified by OSCG
#     # user_id change: update date_start
#         if vals.get('user_id') and not vals.get('date_start'):
#             vals['date_start'] = fields.datetime.now()
    # <<< modified by OSCG

    # context: no_log, because subtype already handle this
    create_context = dict(context, mail_create_nolog=True)
    task_id = super(task, self).create(cr, uid, vals, context=create_context)
    self._store_history(cr, uid, [task_id], context=context)
    return task_id


class TaskHookCreate(models.AbstractModel):
    _name = 'project.task.hook.create'
    _description = 'Provide hook point for create method'

    def _register_hook(self, cr):
        task.create = create
        return super(TaskHookCreate, self)._register_hook(cr)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: