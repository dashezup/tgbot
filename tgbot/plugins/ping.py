import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from ..config import PING_ALLOWED_USERS, PING_DELAY_DELETE


@Client.on_message(filters.private
                   & filters.user(PING_ALLOWED_USERS)
                   & filters.text
                   & ~filters.edited
                   & filters.regex("ping"))
async def ping_pong(_, message: Message):
    reply = await message.reply("pong", quote=True)
    await asyncio.sleep(PING_DELAY_DELETE)
    await reply.delete()
    await message.delete()
