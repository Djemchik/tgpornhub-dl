from pyrogram import Client, idle
from pyrogram.errors import UserNotParticipant
from asyncio import get_event_loop_policy

from .config import API_ID, API_HASH, TOKEN, log_chat


bot = Client(
    name="bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=TOKEN,
    plugins=dict(root="pornhub.plugins"),
    in_memory=True,
)


async def main():
    await bot.start()
    try:
        await bot.send_message(
            log_chat, "✅ <b>PornHub started!</b>\n\n🔖 <b>Version:</b> <code>v1.0 (2022)</code>\n🔥 <b>Pyrogram:</b> <code>v2.0.58</code>",
        )
        print("✅ Bot is active!")
    except UserNotParticipant as e:
        print(f"Error: {e}\n\nPlease make sure if the bot has been added to the log chat and the bot is admin in the group!")
        return
    await idle()


if __name__ == "__main__":
    get_event_loop_policy().get_event_loop().run_until_complete(main())