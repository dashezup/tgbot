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


Upload paste to https://ezup.dev/p

Commands:
- /paste
"""
import os
import socket
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from config import COMMON_CHATS

DELETE_DELAY = 8


@Client.on_message((filters.chat(COMMON_CHATS) | filters.private)
                   & filters.text
                   & ~filters.edited
                   & filters.regex('^/paste$'))
async def upload_paste_to_ezup_pastebin(_, m: Message):
    reply = m.reply_to_message
    if not reply:
        return
    paste_content = await _get_paste_content(reply)
    if not paste_content:
        response = await m.reply_text("ezpaste: invalid", quote=True)
        await _delay_delete_messages([response, m])
        return
    url = await _netcat('ezup.dev', 9999, paste_content)
    if not reply.document:
        await asyncio.sleep(1)
    await reply.reply_text(url, quote=True)
    await m.delete()


async def _get_paste_content(m: Message):
    if m.text:
        return m.text
    elif m.document:
        if m.document.file_size > 4096 \
                or m.document.mime_type.split('/')[0] != 'text':
            return None
        filename = await m.download()
        with open(filename) as f:
            return f.read()
        os.remove(filename)
    else:
        return None


async def _delay_delete_messages(messages: list):
    await asyncio.sleep(DELETE_DELAY)
    for m in messages:
        await m.delete()


async def _netcat(host, port, content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, int(port)))
    s.sendall(content.encode())
    s.shutdown(socket.SHUT_WR)
    while True:
        data = s.recv(4096).decode('utf-8').strip('\n\x00')
        if not data:
            break
        return data
    s.close()
