"""
tgbot, a collection of Pyrogram Smart Plugins for Telegram bots
Copyright (C) 2021  Dash Eclipse

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.


/pin a message and open a pull to decide to repin with notification or not

Required chat permissions in COMMON_CHATS
- can_send_messages
- can_send_polls
- can_pin_messages
"""
import asyncio
from datetime import datetime
from typing import List

from pyrogram import Client, filters, emoji
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup, InlineKeyboardButton,
    CallbackQuery,
    Poll
)

from config import COMMON_CHATS

DELAY_DELETE_IN_SEC = 6
POLL_MAX_AGE_IN_DAY = 2
POLL_MAX_AGE_IN_SEC = POLL_MAX_AGE_IN_DAY * 60 * 60 * 24


@Client.on_message(filters.chat(COMMON_CHATS)
                   & filters.text
                   & filters.regex("^/pin$")
                   & ~filters.edited
                   & ~filters.via_bot)
async def pin_message(_, m: Message):
    m_reply = m.reply_to_message
    if not m_reply:
        resp_text = (
            "Reply to a message to pin it and open a poll for loud pin, "
            f"the poll will be available up for {POLL_MAX_AGE_IN_DAY} days "
            "and the sender of the replied message will be able to "
            "process/ignore the poll result"
        )
    elif not (m_reply.from_user and not m_reply.from_user.is_bot):
        resp_text = "Replied message must be from a user"
    else:
        resp_text = None
    if resp_text:
        resp = await m.reply_text(resp_text)
        await _delay_delete_messages([resp, m])
        return
    if not m.chat.permissions.can_pin_messages:
        member = await m.chat.get_member(m.from_user.id)
        if not member.can_pin_messages:
            resp = await m.reply_text(
                f"{emoji.PROHIBITED} You don't have permission to "
                "pin messages here"
            )
            await _delay_delete_messages([resp, m])
            return
    await m_reply.unpin()
    await m_reply.pin(disable_notification=True)
    await m_reply.reply_poll(
        f"{m.from_user.first_name}: re-pin with notification?",
        ["Yes", "No", "View Result"],
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Process",
                        callback_data="process_pin_poll"
                    ),
                    InlineKeyboardButton(
                        "Ignore",
                        callback_data="ignore_pin_poll"
                    )
                ]
            ]
        )
    )
    await m.delete()


@Client.on_callback_query(filters.regex("^(process|ignore)_pin_poll$"))
async def process_pin_poll(client: Client, cq: CallbackQuery):
    m: Message = cq.message
    m_reply: Message = m.reply_to_message
    poll: Poll = m.poll
    if not (m.from_user.is_self
            and poll
            and m_reply.from_user.id == cq.from_user.id):
        await cq.answer(f"{emoji.PROHIBITED} Invalid or unavailable for you")
        return
    await m.edit_reply_markup(None)
    await client.stop_poll(m.chat.id, m.message_id)
    poll_age = datetime.utcnow().timestamp() - m.date
    if cq.data == "process_pin_poll" \
            and poll.options[0].voter_count > poll.options[1].voter_count \
            and poll_age < POLL_MAX_AGE_IN_SEC:
        await m.reply_to_message.unpin()
        await m.reply_to_message.pin()
        await cq.answer(f"{emoji.BELL} Re-pinned with notification",
                        show_alert=True)
    else:
        await cq.answer(f"{emoji.BELL_WITH_SLASH} Poll closed, no re-pin",
                        show_alert=True)


async def _delay_delete_messages(messages: List[Message]):
    await asyncio.sleep(DELAY_DELETE_IN_SEC)
    for m in messages:
        await m.delete()
