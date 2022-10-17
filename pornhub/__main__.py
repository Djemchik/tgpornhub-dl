from pyrogram import Client, idle
from asyncio import get_event_loop_policy

from .config import API_ID, API_HASH, TOKEN


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
    await idle()


if __name__ == "__main__":
    get_event_loop_policy().get_event_loop().run_until_complete(main())