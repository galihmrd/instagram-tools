import codecs
import os

import telebot
from requests import post

from config import BOT_TOKEN
from main import info, start

session = telebot.TeleBot(BOT_TOKEN)


@session.message_handler(commands=["start", "help"])
def plugin_1(self):
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
        session.send_message(self.chat.id, f"https://nekobin.com/{link}")
        os.remove("dont_follow_me.txt")
    except Exception as e:
        print(e)


# @Client.on_message(filters.command("super-unfollow"))
# async def super_unfoll(client, message):
#    start()
#    super_unfollow()
#    text = codecs.open("super_unfollow.txt", "r+", encoding="utf-8")
#    paste_text = text.read()
#    try:
#        link = (
#            post(
#                "https://nekobin.com/api/documents",
#                json={"content": paste_text},
#            )
#            .json()
#            .get("result")
#            .get("key")
#        )
#        await message.reply(f"https://nekobin.com/{link}")
#    except Exception as e:
#        print(e)

if __name__ == "__main__":
    try:
        session.infinity_polling()
    except Exception:
        time.sleep(15)
