import random
import time
import os
import codecs
import telebot
from requests import post

import aux_funcs
from API.InstagramAPI import InstagramAPI
from config import BOT_TOKEN

followers = []
followings = []

### Delay in seconds ###
min_delay = 5
max_delay = 10
MAXIMO = 100

class User:
    passw = None
    name = None
    API = None

session = telebot.TeleBot(BOT_TOKEN)


@session.message_handler(commands=["info"])
def plugin_1(self):
    info()
    text = codecs.open("dont_follow_me.txt", "r", encoding="utf-8")
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

@session.message_handler(commands=['login'])
def name1(menss):
    name = session.reply_to(menss, "Please enter your username:")
    session.register_next_step_handler(name, passwx)

def passwx(menss):
    User.name = menss.text
    User.chat_id = menss.chat.id
    passw = session.reply_to(menss, "Please enter your password:")
    session.register_next_step_handler(passw, process)

def process(menss):
    User.passw = menss.text
    session.send_message(menss.chat.id, "Just a moment...")
    User.API = InstagramAPI(username=User.name, password=User.passw)
    start(menss)


def info():
    f = open("dont_follow_me.txt", "a")
    f.write("I follow them but they dont follow me:\n")
    tot = 0
    for i in followings:
        if i not in followers:
            tot = tot + 1
            f.write(str(tot) + " " + i)
            f.write("\n")

    f.write("\nTotal: " + str(tot))
    f.write("\n\n")

    f.write("\nThey follow me but i dont follow them:\n")
    tot = 0
    for i in followers:
        if i not in followings:
            tot = tot + 1
            f.write(str(tot) + " " + i)
            f.write("\n")

    f.write("\nTotal: " + str(tot))
    f.write("\n\n")

    f.write("\nPeople following me:\n")
    tot = 0
    for i in followers:
        tot = tot + 1
        f.write(str(tot) + " " + i)
        f.write("\n")

    f.write("\nTotal: " + str(tot))
    f.write("\n\n")

    f.write("\nPeople I follow:\n")
    tot = 0
    for i in followings:
        tot = tot + 1
        f.write(str(tot) + " " + i)
        f.write("\n")

    f.write("\nTotal: " + str(tot))


def follow_tag(tag):
    api.tagFeed(tag)
    media_id = api.LastJson
    tot = 0
    print("\nTAG: " + str(tag) + "\n")
    for i in media_id["items"]:
        time.sleep(float(random.uniform(min_delay * 10, max_delay * 10) / 10))
        username = i.get("user")["username"]
        user_id = i.get("user")["pk"]
        User.API.follow(user_id)
        tot += 1
        print("Following " + str(username) + " (with id " + str(user_id) + ")")
        if tot >= MAXIMO:
            break
    print(
        "Total: " + str(tot) + " for tag " + tag + " (Max val: " + str(MAXIMO) + ")\n"
    )


def follow_location(target):
    api.getLocationFeed(target)
    media_id = api.LastJson
    tot = 0
    for i in media_id.get("items"):
        time.sleep(float(random.uniform(min_delay * 10, max_delay * 10) / 10))
        username = i.get("user").get("username")
        user_id = aux_funcs.get_id(username)
        User.API.follow(user_id)
        tot += 1
        f = open("follow_location.txt", "a")
        f.write("Following " + str(username) + " (with id " + str(user_id) + ")")
        f.write("\n")
        if tot >= MAXIMO:
            break
    print(
        "Total: "
        + str(tot)
        + " for location "
        + str(target)
        + " (Max val: "
        + str(MAXIMO)
        + ")\n"
    )


def follow_list(target):
    user_list = open(target).read().splitlines()
    tot = 0
    for username in user_list:
        time.sleep(float(random.uniform(min_delay * 10, max_delay * 10) / 10))
        user_id = aux_funcs.get_id(username)
        User.API.follow(user_id)
        tot += 1
        f = open("follow_list.txt", "a")
        f.write("Following " + str(username) + " (with id " + str(user_id) + ")")
        f.write("\n")
        if tot >= MAXIMO:
            break
    print(
        "Total: "
        + str(tot)
        + " users followed from "
        + str(target)
        + " (Max val: "
        + str(MAXIMO)
        + ")\n"
    )


def super_followback():
    count = 0
    for i in followers:
        if i not in followings:
            count += 1
            time.sleep(float(random.uniform(min_delay * 10, max_delay * 10) / 10))
            f = open("super_followback.txt", "a")
            f.write(str(count) + ") Following back " + i)
            f.write("\n")
            user_id = aux_funcs.get_id(i)
            User.API.follow(user_id)


def super_unfollow():
    whitelist = open("whitelist.txt").read().splitlines()
    count = 0
    for i in followings:
        if (i not in followers) and (i not in whitelist):
            count += 1
            time.sleep(float(random.uniform(min_delay * 10, max_delay * 10) / 10))
            f = open("super_unfollow.txt", "a")
            f.write(str(count) + ") Unfollowing " + i)
            f.write("\n")
            user_id = aux_funcs.get_id(i)
            User.API.unfollow(user_id)


# def unfollowall():
#    whitelist = open("whitelist.txt").read().splitlines()
#    count = 0
#    for i in followings:
#        if i not in whitelist:
#            count += 1
#            time.sleep(float(random.uniform(min_delay * 10, max_delay * 10) / 10))
#            print(str(count) + ") Unfollowing " + i)
#            user_id = aux_funcs.get_id(i)
#            api.unfollow(user_id)


def start(self):
    try:
       User.API.login()
       for i in User.API.getTotalSelfFollowers():
           followers.append(i.get("username"))
       for i in User.API.getTotalSelfFollowings():
           followings.append(i.get("username"))
       session.send_message(self.chat.id, "Login successfully")
    except Exception as e:
       session.send_message(self.chat.id, f"Login Failed...\nLog: {e}")

if __name__ == "__main__":
    try:
        print("Started...!")
        session.infinity_polling()
    except Exception:
        time.sleep(15)
