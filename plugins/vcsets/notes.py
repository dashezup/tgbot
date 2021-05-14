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


Pyrogram Smart Plugin for notes in t.me/VCSets

Required chat permission:
- Delete messages
"""
import json
import pathlib
from pyrogram import Client, filters
from pyrogram.types import Message

response = {}
parent_path = pathlib.Path(__file__).parent.absolute()
json_file = pathlib.PurePath.joinpath(parent_path, 'notes.json')
with open(json_file) as f:
    notes = json.load(f)


@Client.on_message(
    filters.chat("VCSets")
    & filters.text
    & ~filters.edited
    & (filters.command(list(notes.keys()), prefixes="#")
       | filters.command(["notes", "notes@ezupdevbot"], prefixes="/"))
)
async def show_notes(_, m: Message):
    if len(m.command) != 1:
        return
    section = m.command[0].split("@")[0]
    m_target, quote = (m.reply_to_message or m), bool(m.reply_to_message)
    m_response = await m_target.reply_text(
        notes[section],
        quote=quote,
        disable_web_page_preview=True
    )
    await m.delete()
    key = 'list' if section == 'notes' else 'note'
    if response.get(key) is not None:
        await response[key].delete()
    response[key] = m_response
