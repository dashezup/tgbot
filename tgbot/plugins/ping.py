"""reply ping with pong

# ../config.py
# int | str | list
PING_CHATS = -1234567890123
# int | str | list
PING_USERS = 1234567890
PING_DELAY_DELETE = 8

"""
import asyncio
from time import time
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message
from ..config import PING_CHATS, PING_USERS, PING_DELAY_DELETE

START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ('week', 60 * 60 * 24 * 7),
    ('day', 60 * 60 * 24),
    ('hour', 60 * 60),
    ('min', 60),
    ('sec', 1)
)


# https://gist.github.com/borgstrom/936ca741e885a1438c374824efb038b3
def _human_time_duration(seconds):
    if seconds == 0:
        return 'inf'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'
                         .format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)


@Client.on_message(filters.text
                   & (filters.chat(PING_CHATS) | filters.user(PING_USERS))
                   & filters.incoming
                   & ~filters.edited
                   & filters.regex("ping"))
async def ping_pong(_, message: Message):
    """reply ping with pong and delete both messages"""
    start = time()
    reply = await message.reply_text("...", quote=True)
    delta_ping = time() - start
    await reply.edit_text(f"**Pong!** `{delta_ping * 1000:.3f} ms`")
    await _delay_delete_messages((reply, message), PING_DELAY_DELETE)


@Client.on_message(filters.text
                   & (filters.chat(PING_CHATS) | filters.user(PING_USERS))
                   & filters.incoming
                   & ~filters.edited
                   & filters.regex("uptime"))
async def get_uptime(_, message: Message):
    """/uptime Reply with readable uptime and ISO 8601 start time"""
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = _human_time_duration(int(uptime_sec))
    reply = await message.reply_text(f"uptime: `{uptime}`\n"
                                     f"start time: `{START_TIME_ISO}`",
                                     quote=True)
    await _delay_delete_messages((reply, message), PING_DELAY_DELETE)


async def _delay_delete_messages(messages: tuple, delay: int):
    await asyncio.sleep(delay)
    for msg in messages:
        await msg.delete()
