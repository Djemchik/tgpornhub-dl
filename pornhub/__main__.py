from pyrogram import Client
from pyrogram.methods.utilities.idle import idle
from asyncio import get_event_loop_policy

from .config import API_ID, API_HASH, TOKEN


bot = Client(
    name="bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=TOKEN,
    in_memory=True,
)


async def main():
    async with bot:
        await idle()


if __name__ == "__main__":
    get_event_loop_policy().get_event_loop().run_until_complete(main())