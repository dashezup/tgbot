"""commands which starts with slash /"""
from pyrogram import Client, filters
from pyrogram.types import Message
from ..config import COMMANDS_CHATS, COMMANDS_TEXT_START, COMMANDS_TEXT_HELP


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
