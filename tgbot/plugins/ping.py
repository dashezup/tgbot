"""reply ping with pong"""
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from ..config import PING_DELAY_DELETE


@Client.on_message(filters.private
                   & filters.text
                   & filters.incoming
                   & ~filters.edited
                   & filters.regex("ping"))
async def ping_pong(_, message: Message):
    """reply ping with pong and delete both messages"""
    reply = await message.reply("pong", quote=True)
    await asyncio.sleep(PING_DELAY_DELETE)
    await reply.delete()
    await message.delete()
