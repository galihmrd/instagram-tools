import logging, os
from pyrogram import Client, idle
from config import API_HASH, API_ID, BOT_TOKEN


if os.path.exists("log.txt"):
    with open("log.txt", "r+") as f:
        f.truncate(0)

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="[%X]",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

bot = Client(
    ":memory:",
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="Telegram_client"),
)

bot.start()
idle()
