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


Call admin when someone send a message which starts with @admin
Requires Python 3.9+

# ../config.py
CALL_ADMIN_CHATS = -1234567890
# int
CALL_ADMIN_ADMINS = [456789]
"""
from pyrogram import Client, filters
from pyrogram.types import Message
from config import CALL_ADMIN_CHATS, CALL_ADMIN_ADMINS


@Client.on_message(filters.command("admin", "@")
                   & filters.chat(CALL_ADMIN_CHATS)
                   & filters.incoming
                   & ~filters.edited)
async def call_admin(client, message: Message):
    if message.sender_chat or (message.reply_to_message
                               and message.reply_to_message.sender_chat):
        return
    u_call = message.from_user
    await message.reply_text(f"Hey admins, {u_call.mention()} "
                             "asked me to call you!")
    text = message.text.markdown.removeprefix('@admin').removeprefix(' ')
    m_link = message.link
    for user in CALL_ADMIN_ADMINS:
        await client.send_message(
            user,
            f"**{u_call.mention()}**: "
            f"{text}\n{m_link}"
        )
