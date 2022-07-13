import os
from pyrogram import Client, filters
from pyrogram.types import Message
from main import info, start


@Client.on_message(filters.command("start"))
async def plugin_1(client, message):
    chat_id = message.from_user.id
    start()
    info()
