from pyrogram.types import Message
from pyrogram import Client, filters
from config import KUKI_API, CHATBOT_NAME, OWNER_NAME

from kukiapipy import kuki as ai


@Client.on_message(
    filters.text
    & filters.reply
    & ~filters.bot
    & ~filters.edited,
    group=2,
)
async def chat_bot(client, message):
    chat_id = message.chat.id
    process = ai.chatbot(
                  key = KUKI_API,
                  name = CHATBOT_NAME,
                  owner = OWNER_NAME,
                  msg = message.text
    )
    await client.send_chat_action(chat_id, "typing")
    await message.reply(process)
