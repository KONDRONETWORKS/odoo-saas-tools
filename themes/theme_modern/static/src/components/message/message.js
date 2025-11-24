/** @odoo-module **/

import { Message } from '@mail/components/message/message';
import { session } from "@web/session";
import { patch } from '@web/core/utils/patch';

const { useState } = owl;

var user = session.partner_id

patch(Message.prototype, {

    /**
     * Get the date time of the message at current user locale time.
     *
     * @returns {string}
     */
    get user_id() {
        return user;
    },
});
