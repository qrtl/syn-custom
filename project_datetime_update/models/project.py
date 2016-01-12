# -*- coding: utf-8 -*-
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 Rooms For (Hong Kong) Limited T/A OSCG
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
from openerp import tools
from openerp.tools.translate import _

class project_task_type(osv.osv):
    _inherit = 'project.task.type'

    _columns = {
        'stage_start': fields.boolean('Stage assigned to Start'),
        'stage_end': fields.boolean('Stage assigned to End'),
    }

class Task(osv.osv):
    _inherit = "project.task"

    def create(self, cr, uid, vals, context=None):
        context = dict(context or {})

        # for default stage
        if vals.get('project_id') and not context.get('default_project_id'):
            context['default_project_id'] = vals.get('project_id')
        # user_id change: update date_start
#        if vals.get('user_id') and not vals.get('date_start'):
#            vals['date_start'] = fields.datetime.now()

        # context: no_log, because subtype already handle this
        create_context = dict(context, mail_create_nolog=True)
        task_id = super(Task, self).create(cr, uid, vals, context=create_context)
        self._store_history(cr, uid, [task_id], context=context)
        return task_id

    def write(self, cr, uid, ids, vals, context=None):
        if isinstance(ids, (int, long)):
            ids = [ids]

        # stage change: update date_last_stage_update
        if 'stage_id' in vals:
            vals['date_last_stage_update'] = fields.datetime.now()

        # stage change: update date_start
        if 'stage_id' in vals:
            if self.pool.get('project.task.type').browse(cr, uid, [vals['stage_id']])[0].stage_start:
                vals['date_start'] = fields.datetime.now()

        # stage change: update date_end
        if 'stage_id' in vals: 
            if self.pool.get('project.task.type').browse(cr, uid, [vals['stage_id']])[0].stage_end:
                vals['date_end'] = fields.datetime.now()

        # user_id change: update date_start
#        if vals.get('user_id') and 'date_start' not in vals:
#            vals['date_start'] = fields.datetime.now()

        # Overridden to reset the kanban_state to normal whenever
        # the stage (stage_id) of the task changes.
        if vals and not 'kanban_state' in vals and 'stage_id' in vals:
            new_stage = vals.get('stage_id')
            vals_reset_kstate = dict(vals, kanban_state='normal')
            for t in self.browse(cr, uid, ids, context=context):
                write_vals = vals_reset_kstate if t.stage_id.id != new_stage else vals
                super(Task, self).write(cr, uid, [t.id], write_vals, context=context)
            result = True
        else:
            result = super(Task, self).write(cr, uid, ids, vals, context=context)

        if any(item in vals for item in ['stage_id', 'remaining_hours', 'user_id', 'kanban_state']):
            self._store_history(cr, uid, ids, context=context)
        return result


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

