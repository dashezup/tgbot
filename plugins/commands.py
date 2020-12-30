"""commands which starts with slash /

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
    MUSIC_INFORM_AVAILABILITY
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
