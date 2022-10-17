from typing import Union
from pyrogram import Client, filters
from pyrogram.errors import MessageNotModified, QueryIdInvalid
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from ..config import prefixs, sub_chat, sudoers


sudofilter = filters.user(sudoers)

button_a1 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="✅ Agree & Continue",
                callback_data="final_page",
            )
        ],[
            InlineKeyboardButton(
                text="❌ Cancel",
                callback_data="home_intro",
            ),
        ],
    ]
)


button_a2 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="search here", switch_inline_query_current_chat="",
            )
        ],[
            InlineKeyboardButton(
                text="search in chat", switch_inline_query="",
            ),
        ],
    ]
)


@Client.on_message(filters.command("start", prefixs) & filters.private)
@Client.on_callback_query(filters.regex("^home_intro$"))
async def intro_msg(_, update: Union[Message, CallbackQuery]):
    if isinstance(update, CallbackQuery):
        try:
            await update.answer()
        except QueryIdInvalid:
            pass
        method = update.edit_message_text
    else:
        method = update.reply_text
    
    value = str(update.chat.id)
    with open("users.txt", "a+") as file:
        file.seek(0)
        line = file.read().splitlines()
        if value in line:
            print(f"User: {value} is using the bot")
        else:
            file.write(value + "\n")

    text = f"Hi {update.from_user.first_name}!\n\nUse this bot to download videos from the pornhub.com site by providing the name of the video you want to download or you can also search for the video you want to download via inline mode.\n\nJoin the redirected channel in order to use this bot!"
    button = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "• Channel •", url=f"https://t.me/{sub_chat}",
                )
            ],[
                InlineKeyboardButton(
                    "Terms of use & Privacy", callback_data="terms",
                ),
            ],
        ]
    )

    try:
        await method(text, reply_markup=button)
    except MessageNotModified:
        pass


@Client.on_callback_query(filters.regex("^terms$"))
async def terms_panel(_, q: CallbackQuery):
    await q.answer("Read the terms of use & user privacy!")
    text = """
🧸 <u><b>PornHub bot</b></u>

⚠️ <b>WARNING !</b>
This bot contains 18+ content, make sure you are an adult user to be able to use this bot!. Reporting this bot will get it blocked by Telegram, so if you're considering sticking with bots, don't do it!

🔐 <b>Privacy Policy</b>
We ensure that your search data in this bot is protected safely.  Whoever you are, whenever and wherever you use this bot to download videos from pornhub, you don't have to be afraid of spreading it to the public.

<i>You don't have to worry, because our bot staff will make sure that your data is well protected and safe.</i>

👉🏻 Press the <b>green button</b> to declare that you have <b>read and accepted these conditions</b> to use this bot, otherwise cancel.
    """
    await q.edit_message_text(text, reply_markup=button_a1)


@Client.on_callback_query(filters.regex("^final_page$"))
async def greets(_, q: CallbackQuery):
    await q.answer("Thanks for agreeing to the bot policy!")
    await q.edit_message_text(
        f"Hi {q.from_user.first_name}!\n\nYou can browse this bot now!",
        reply_markup=button_a2,
    )


@Client.on_message(filters.command("files", prefixs))
async def show_files(_, update: Message):
    files = os.listdir("downloads")
    await update.reply(files)


@Client.on_message(filters.command("stats", prefixs) & sudofilter)
async def bot_statistic(_, update: Message):
    users = open("member.txt").readlines()
    stats = open("member.txt").read()
    total = len(users)
    await update.reply_text(f"Total: {total} users")
    await update.reply_text(f"{stats}")


@Client.on_message(filters.command("gcast", prefixs) & sudofilter)
async def broadcast(_, update: Message):
    if update.reply_to_message.text:
        await update.reply_text("Broadcasting...")
        query = open("member.txt").readlines()
        for row in query:
            try:
                resp = update.reply_to_message
                await resp.copy(row)
            except Exception:
                pass
    else:
        await update.reply_text("Other message type like sticker, photo, etc; are not supported!")


@Client.on_message(filters.command("help", prefixs))
async def command_list(_, update: Message):
    text_1 = """
🛠 Command list:

» /start - start this bot
» /help  - showing this message
» /ping  - check bot status
» /files - show downloaded files
    """
    text_2 = """
🛠 Command list:

» /start - start this bot
» /help  - showing this message
» /ping  - check bot status
» /files - show downloaded files
» /stats - show bot statistic
» /gcast - broadcast message
    """
    if update.from_user.id in sudoers:
        await update.reply_text(text_1)
    else:
        await update.reply_text(text_2)