from pyrogram import Client, idle
from config import API_HASH, API_ID, BOT_TOKEN


bot = Client(
    ':memory:',
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="lib.plugins"),
)

bot.start()
print("Bot started!")
idle()
