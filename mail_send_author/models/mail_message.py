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

from openerp.osv import osv
from openerp import SUPERUSER_ID, api

class mail_message(osv.Model):
    _inherit = 'mail.message'

    @api.cr_uid_ids_context
    def set_message_read(self, cr, uid, msg_ids, read, create_missing=True, context=None):
        """ Set messages as (un)read. Technically, the notifications related
            to uid are set to (un)read. If for some msg_ids there are missing
            notifications (i.e. due to load more or thread parent fetching),
            they are created.

            :param bool read: set notification as (un)read
            :param bool create_missing: create notifications for missing entries
                (i.e. when acting on displayed messages not notified)

            :return number of message mark as read
        """
        notification_obj = self.pool.get('mail.notification')
        user_pid = self.pool['res.users'].browse(cr, SUPERUSER_ID, uid, context=context).partner_id.id
        domain = [('partner_id', '=', user_pid), ('message_id', 'in', msg_ids)]
        if not create_missing:
            domain += [('is_read', '=', not read)]
        notif_ids = notification_obj.search(cr, uid, domain, context=context)
# start addition
        if context.get('mail_read_set_read'):
            if msg_ids:
                messages = self.browse(cr, uid, msg_ids[0], context=context)
                user_partner = self.pool.get('res.partner').browse(cr, uid, user_pid, context=context)
                if messages.author_id.email == user_partner.email:
                    return len(notif_ids)
# end addition

        # all message have notifications: already set them as (un)read
        if len(notif_ids) == len(msg_ids) or not create_missing:
            notification_obj.write(cr, uid, notif_ids, {'is_read': read}, context=context)
            return len(notif_ids)

        # some messages do not have notifications: find which one, create notification, update read status
        notified_msg_ids = [notification.message_id.id for notification in notification_obj.browse(cr, uid, notif_ids, context=context)]
        to_create_msg_ids = list(set(msg_ids) - set(notified_msg_ids))
        for msg_id in to_create_msg_ids:
            notification_obj.create(cr, uid, {'partner_id': user_pid, 'is_read': read, 'message_id': msg_id}, context=context)
        notification_obj.write(cr, uid, notif_ids, {'is_read': read}, context=context)
        return len(notif_ids)


    def _notify(self, cr, uid, newid, context=None, force_send=False, user_signature=True):
        """ Add the related record followers to the destination partner_ids if is not a private message.
            Call mail_notification.notify to manage the email sending
        """
        notification_obj = self.pool.get('mail.notification')
        message = self.browse(cr, SUPERUSER_ID, newid, context=context)
        partners_to_notify = set([])

        # all followers of the mail.message document have to be added as partners and notified if a subtype is defined (otherwise: log message)
        if message.subtype_id and message.model and message.res_id:
            fol_obj = self.pool.get("mail.followers")
            # browse as SUPERUSER because rules could restrict the search results
            fol_ids = fol_obj.search(
                cr, SUPERUSER_ID, [
                    ('res_model', '=', message.model),
                    ('res_id', '=', message.res_id),
                ], context=context)
            partners_to_notify |= set(
                fo.partner_id.id for fo in fol_obj.browse(cr, SUPERUSER_ID, fol_ids, context=context)
                if message.subtype_id.id in [st.id for st in fo.subtype_ids]
            )
        # remove me from notified partners, unless the message is written on my own wall
        if message.subtype_id and message.author_id and message.model == "res.partner" and message.res_id == message.author_id.id:
            partners_to_notify |= set([message.author_id.id])
#        elif message.author_id:
#            partners_to_notify -= set([message.author_id.id])

        # all partner_ids of the mail.message have to be notified regardless of the above (even the author if explicitly added!)
        if message.partner_ids:
            partners_to_notify |= set([p.id for p in message.partner_ids])

        # notify
        notification_obj._notify(
            cr, uid, newid, partners_to_notify=list(partners_to_notify), context=context,
            force_send=force_send, user_signature=user_signature
        )
        message.refresh()

        # An error appear when a user receive a notification without notifying
        # the parent message -> add a read notification for the parent
        if message.parent_id:
            # all notified_partner_ids of the mail.message have to be notified for the parented messages
            partners_to_parent_notify = set(message.notified_partner_ids).difference(message.parent_id.notified_partner_ids)
            for partner in partners_to_parent_notify:
                notification_obj.create(cr, uid, {
                        'message_id': message.parent_id.id,
                        'partner_id': partner.id,
                        'is_read': True,
                    }, context=context)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
