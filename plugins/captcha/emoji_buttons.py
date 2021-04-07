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


A Pyrogram Smart Plugin to verify if new members are human
Provide 4 random emojis for new members to press the correct button
to verify

# ../config.py
# int | str | list
# the bot must be admin in the chat
WELCOME_CHATS = -1234567890123
# should not be lesser than 0.5 or the user may be banned if he didn't
# press the verification button
# recommend value: integer 2 or greater
WELCOME_DELAY_KICK_MIN = 2

"""
import random
import asyncio
from datetime import datetime
from pyrogram import Client, filters, emoji
from pyrogram.types import (
    Message, User, Chat,
    CallbackQuery,
    InlineKeyboardMarkup, InlineKeyboardButton,
    ChatPermissions
)
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from config import WELCOME_CHATS, WELCOME_DELAY_KICK_MIN

WELCOME_DELAY_KICK_SEC = WELCOME_DELAY_KICK_MIN * 60
ALL_EMOJI_NAMES = [i for i in dir(emoji) if not i.startswith('__')]


@Client.on_message(filters.chat(WELCOME_CHATS) & filters.new_chat_members)
async def welcome(_, m: Message):
    """Mute new member and send message with button"""
    for user in m.new_chat_members:
        await verify_new_member(m, user)


async def verify_new_member(m: Message, user: User):
    await m.chat.restrict_member(user.id, ChatPermissions())
    text, reply_markup = await generate_captcha(user)
    m_btn = await m.reply(
        text,
        reply_markup=reply_markup,
        quote=True
    )
    await kick_restricted_after_delay(WELCOME_DELAY_KICK_SEC, m_btn)


async def generate_captcha(user: User):
    correct_emoji = getattr(emoji, random.choice(ALL_EMOJI_NAMES))
    buttons = [
        InlineKeyboardButton(correct_emoji, callback_data="captcha_success")
    ] + [
        InlineKeyboardButton(getattr(emoji, i), callback_data="captcha_fail")
        for i in random.sample(ALL_EMOJI_NAMES, 3)
    ]
    random.shuffle(buttons)
    text = (f"Welcome, {user.mention}\n**Are you human?**\n"
            f"Press the button which contains {correct_emoji} to verify\n\n"
            "__You will be removed from this chat if you are not verified "
            f"in **{WELCOME_DELAY_KICK_MIN}** min__")
    reply_markup = InlineKeyboardMarkup([buttons])
    return (text, reply_markup)


@Client.on_callback_query(filters.regex("^captcha_(success|fail)$"))
async def callback_query_captcha(_, cq: CallbackQuery):
    m_btn = cq.message
    entities = m_btn.entities
    if not (entities and entities[0].type == "text_mention"):
        return
    captcha_result = cq.data.removeprefix("captcha_")
    if cq.from_user.id == entities[0].user.id:
        if captcha_result == "success":
            await cq.answer("Congrats, verification passed!")
            await m_btn.chat.unban_member(cq.from_user.id)
        else:
            await cq.answer("Wrong choice, you will be banned "
                            f"for {WELCOME_DELAY_KICK_MIN} min")
            await asyncio.sleep(3)
            await _ban_restricted_user_until_date(
                m_btn.chat,
                cq.from_user.id,
                duration=WELCOME_DELAY_KICK_SEC
            )
        await m_btn.delete()
        # await m_btn.reply_to_message.delete()
    else:
        await cq.answer(f"This is for {entities[0].user.first_name}")


async def kick_restricted_after_delay(delay: int, button_message: Message):
    """If the new member is still restricted after the delay, delete
    button message and join message and then kick him
    """
    await asyncio.sleep(delay)
    join_message = button_message.reply_to_message
    group_chat = button_message.chat
    user_id = join_message.from_user.id
    await join_message.delete()
    await button_message.delete()
    await _ban_restricted_user_until_date(group_chat, user_id, duration=delay)


@Client.on_message(filters.chat(WELCOME_CHATS) & filters.left_chat_member)
async def left_chat_member(_, message: Message):
    """When a restricted member left the chat, ban him for a while"""
    group_chat = message.chat
    user_id = message.left_chat_member.id
    await _ban_restricted_user_until_date(group_chat, user_id,
                                          duration=WELCOME_DELAY_KICK_SEC)


async def _ban_restricted_user_until_date(group_chat: Chat,
                                          user_id: int,
                                          duration: int):
    try:
        member = await group_chat.get_member(user_id)
        if member.status == "restricted":
            until_date = int(datetime.utcnow().timestamp() + duration)
            await group_chat.kick_member(user_id, until_date=until_date)
    except UserNotParticipant:
        pass
