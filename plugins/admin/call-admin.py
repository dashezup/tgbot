"""Call admin when someone send a message which starts with @admin
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
