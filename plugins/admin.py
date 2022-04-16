"""admin actions

Commands:
!kick
!ban
!unban

# ../config.py
# int | str | list
ADMIN_CHATS = -1234567890123
"""
import asyncio
from time import time
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import UserNotParticipant
from config import ADMIN_CHATS

# should be more than 30 seconds
# or less than 366 days
DURATION_UNTIL_UNBAN = 60
DELAY_DELETE = 15


async def admin_action(_, __, message: Message) -> bool:
    """Disallow:
    1. sender_chat (channel or anonymous admin) instead of from_user
    2. mention itself (!command @bot_self_username)
    Accept:
    1. reply a message with exactly !command and not his own message
    2. !command @mention (and not a reply) and not mention himself
    """
    print(message)
    if message.sender_chat or message.mentioned:
        return False
    if not (message.reply_to_message or message.entities):
        return False
    if message.reply_to_message and message.entities:
        return False
    if message.reply_to_message:
        if message.reply_to_message.sender_chat:
            return False
        u_target = message.reply_to_message.from_user
    if message.entities:
        if len(message.entities) > 1 \
                or message.entities[0].type != "text_mention":
            return False
        u_target = message.entities[0].user

    if u_requester.id == u_target.id:
        return False
    admin = ("creator", "administrator")
    if (await message.chat.get_member(u_requester.id)).status in admin:
        return True
    return False

filter_admin_action = filters.create(admin_action)


@Client.on_message(filters.command(["kick"], prefixes="!")
                   & filters.chat(ADMIN_CHATS)
                   & filter_admin_action
                   & filters.incoming
                   & ~filters.edited)
async def kick_user(_, message: Message):
    """!kick admin kick user"""
    # print(message)
    print("placeholder for !kick")
    return
    # error = await _error_disallowed_admin_action(message)
    # if error is not None:
    #     reply = await message.reply_text(f"**ERROR**: {error}")
    #     await _delay_delete_messages((reply, message), DELAY_DELETE)
    #     return
    reason = " ".join(message.command[1:])
    u_proposer = message.from_user
    u_target = message.reply_to_message.from_user
    await message.chat.kick_member(u_target.id,
                                   int(time() + DURATION_UNTIL_UNBAN))
    await message.reply_text("{} kicked {}\n**Reason**: {}"
                             .format(u_proposer.mention,
                                     u_target.mention,
                                     reason))
    await message.delete()


@Client.on_message(filters.command(["ban"], prefixes="!")
                   & filters.chat(ADMIN_CHATS)
                   & filters.incoming
                   & ~filters.edited)
async def ban_user(_, message: Message):
    """!ban admin ban members"""
    error = await _error_disallowed_admin_action(message)
    if error is not None:
        reply = await message.reply_text(f"**ERROR**: {error}")
        await _delay_delete_messages((reply, message), DELAY_DELETE)
        return
    reason = " ".join(message.command[1:])
    u_proposer = message.from_user
    u_target = message.reply_to_message.from_user
    await message.chat.kick_member(u_target.id)
    await message.reply_text("{} banned {}\n**Reason**: {}"
                             .format(u_proposer.mention,
                                     u_target.mention,
                                     reason))
    await message.delete()


@Client.on_message(filters.command(["unban"], prefixes="!")
                   & filters.chat(ADMIN_CHATS)
                   & filters.incoming
                   & ~filters.edited)
async def unban_user(_, message: Message):
    """!unban admin unban members"""
    error = await _error_disallowed_admin_action(message)
    if error is not None:
        reply = await message.reply_text(f"**ERROR**: {error}")
        await _delay_delete_messages((reply, message), DELAY_DELETE)
        return
    reason = " ".join(message.command[1:])
    u_proposer = message.from_user
    u_target = message.reply_to_message.from_user
    await message.chat.unban_member(u_target.id)
    reply = ("{} unbanned {}\n**Reason**: {}"
             .format(u_proposer.mention, u_target.mention, reason))
    await message.reply_text(reply)
    await message.delete()


async def _error_disallowed_admin_action(message: Message):
    """Return None when none of the condition meet"""
    print(message)
    if message.sender_chat:
        return "Sender is chat not user"
    if not message.reply_to_message:
        return "Reply to a message to take action on the member"
    if message.reply_to_message.sender_chat:
        return "Target is not user"
    # elif len(message.command) == 1:
    #     return False
    c_group = message.chat
    admin = ("creator", "administrator")
    try:
        u_target_id = message.reply_to_message.from_user.id
        member_target = await c_group.get_member(u_target_id)
        if member_target.status in admin:
            return "Target user can't be admin!"
        member_proposer = await c_group.get_member(message.from_user.id)
        if member_proposer.status not in admin:
            return "You are not admin"
    except UserNotParticipant:
        return "Target user is not member of this chat"
    return


async def _delay_delete_messages(messages: tuple, delay: int):
    await asyncio.sleep(delay)
    for m in messages:
        await m.delete()
