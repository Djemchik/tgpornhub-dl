import sys
import httpx
import asyncio
import logging
import platform

from .bot import PornHub
from pyrogram import idle


logging.basicConfig(
    level=logging.INFO,
    format="%(name)s.%(funcName)s | %(levelname)s | %(message)s",
    datefmt="[%X]",
)
logging.getLogger("pyrogram.syncer").setLevel(logging.WARNING)
logging.getLogger("pyrogram.client").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


timeout = httpx.Timeout(40, pool=None)
http = httpx.AsyncClient(http2=True, timeout=timeout)


try:
    import uvloop

    uvloop.install()
except ImportError:
    if platform.system() != "Windows":
        logger.warning("uvloop is not installed and therefore will be disabled.")


async def main():
    pornhub = PornHub()

    try:
        await pornhub.start()

        if "test" not in sys.argv:
            await idle()
    except KeyboardInterrupt:
        logger.warning("Forced stop, Bye!")
    finally:
        await pornhub.stop()
        await http.aclose()


if __name__ == "__main__":
    # open new asyncio event loop
    add_event_loop = asyncio.get_event_loop_policy()
    set_event_loop = add_event_loop.new_event_loop()
    asyncio.set_event_loop(set_event_loop)

    # start the bot
    set_event_loop.run_until_complete(main())

    # close asyncio event loop
    set_event_loop.close()