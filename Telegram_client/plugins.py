import os
import codecs
from requests import get, post
from pyrogram import Client, filters
from pyrogram.types import Message
from main import info, start, super_unfollow


@Client.on_message(filters.command("start"))
async def plugin_1(client, message):
    start()
    info()
    text = codecs.open("dont_follow_me.txt", "r+", encoding="utf-8")
    paste_text = text.read()
    try:
        link = (
            post(
                "https://nekobin.com/api/documents",
                json={"content": paste_text},
            )
            .json()
            .get("result")
            .get("key")
        )
        await message.reply(f"https://nekobin.com/{link}")
        os.remove("dont_follow_me.txt")
    except Exception as e:
        print(e)


@Client.on_message(filters.command("super-unfollow"))
async def super_unfoll(client, message):
    start()
    super_unfollow()
    text = codecs.open("super_unfollow.txt", "r+", encoding="utf-8")
    paste_text = text.read()
    try:
        link = (
            post(
                "https://nekobin.com/api/documents",
                json={"content": paste_text},
            )
            .json()
            .get("result")
            .get("key")
        )
        await message.reply(f"https://nekobin.com/{link}")
    except Exception as e:
        print(e)
