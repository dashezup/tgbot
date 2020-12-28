"""A Pyrogram Smart Plugin to verify if new members are human"""
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.types import ChatPermissions
from ..config import WELCOME_CHATS, WELCOME_DELAY_KICK_MIN

WELCOME_DELAY_KICK_SEC = WELCOME_DELAY_KICK_MIN * 60


@Client.on_message(filters.chat(WELCOME_CHATS) & filters.new_chat_members)
async def welcome(_, message: Message):
    """Mute new member and send message with button"""
    new_members = [f"{u.mention}" for u in message.new_chat_members]
    text = (f"Welcome, {', '.join(new_members)}\n**Are you human?**\n"
            "You will be removed from this chat if you are not verified "
            f"in {WELCOME_DELAY_KICK_MIN} minutes")
    await message.chat.restrict_member(message.from_user.id, ChatPermissions())
    button_message = await message.reply(
        text,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Press Here to Verify",
                        callback_data="pressed_button"
                    )
                ]
            ]
        ),
        quote=True
    )
    await kick_restricted_after_delay(WELCOME_DELAY_KICK_SEC, button_message)


@Client.on_callback_query(filters.regex("pressed_button"))
async def callback_query_welcome_button(_, callback_query):
    """After the new member press the button, set his permissions to
    chat permissions, delete button message and join message
    """
    button_message = callback_query.message
    join_message = button_message.reply_to_message
    group_chat = button_message.chat
    group_permissions = group_chat.permissions
    pending_user = join_message.from_user
    pending_user_id = pending_user.id
    pressed_user_id = callback_query.from_user.id
    if pending_user_id == pressed_user_id:
        await callback_query.answer("Congrats, verification passed!")
        await group_chat.restrict_member(pending_user_id, group_permissions)
        await button_message.delete()
        await join_message.delete()
    else:
        await callback_query.answer(f"This is for {pending_user.first_name}")


async def kick_restricted_after_delay(delay, button_message: Message):
    """If the new member is still restricted after the day, delete
    button message and join message and then kick him
    """
    await asyncio.sleep(delay)
    join_message = button_message.reply_to_message
    group_chat = button_message.chat
    user_id = join_message.from_user.id
    await join_message.delete()
    await button_message.delete()
    if (await group_chat.get_member(user_id)).status == "restricted":
        await group_chat.kick_member(user_id)
        await group_chat.unban_member(user_id)
