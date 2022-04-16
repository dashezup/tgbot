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


Commands which starts with slash /

# ../config
COMMANDS_CHATS = MUSIC_CHATS
COMMANDS_TEXT_START = (
    "This is a music downloader bot for "
    "members of the channel and group"
)
COMMANDS_TEXT_CONTACTS = (
    "Regarding any issues with the bot "
    "feel free to contact"
)
COMMANDS_TEXT_HELP = (
    COMMANDS_TEXT_START
    + "\n\n<b>Usage</b>:\n"
    "- Send a message that only contains a YouTube/SoundCloud/Mixcloud link "
    "to download the music\n"
    "- Playlists are not supported\n"
    "- Your message will be deleted in private chat after the music gets "
    "successfully uploaded\n"
    "- You can get YouTube links with inline bot @vid\n\n"
    + COMMANDS_TEXT_CONTACTS
)
"""
from pyrogram import Client, filters
from pyrogram.types import Message
from config import COMMANDS_CHATS, COMMANDS_TEXT_START, COMMANDS_TEXT_HELP


@Client.on_message(filters.command(["start"])
                   & (filters.chat(COMMANDS_CHATS) | filters.private)
                   & filters.incoming
                   & ~filters.edited)
async def command_start(_, message: Message):
    """/start introduction of the bot"""
    await message.reply(COMMANDS_TEXT_START)


@Client.on_message(filters.command(["help"])
                   & (filters.chat(COMMANDS_CHATS) | filters.private)
                   & filters.incoming
                   & ~filters.edited)
async def command_help(_, message: Message):
    """/help usage of the bot"""
    await message.reply(COMMANDS_TEXT_HELP)


@Client.on_message(filters.command(["json"])
                   & (filters.chat(COMMANDS_CHATS) | filters.private)
                   & filters.incoming
                   & ~filters.edited)
async def command_json(_, message: Message):
    """/json get user info"""
    await message.reply(f"<code>{message}</code>")


@Client.on_message(filters.command(["id"])
                   & (filters.chat(COMMANDS_CHATS) | filters.private)
                   & filters.incoming
                   & ~filters.edited)
async def command_id(_, message: Message):
    """/id get user info"""
    await message.reply(f"<code>{message.from_user}</code>")
