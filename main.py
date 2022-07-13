import os
import asyncio
import aux_funcs, sys, json, time, random
from API.InstagramAPI import InstagramAPI
from config import INSTA_UNAME, INSTA_PW
from pyrogram import Client
from pyrogram.types import Message


followers = []
followings = []
API  = InstagramAPI(INSTA_UNAME, INSTA_PW)

### Delay in seconds ###
min_delay = 5
max_delay = 10
MAXIMO = 100

def printUsage():
	print("Usage: \n+ python main.py -u USERNAME -p PASSWORD -o info: Show report")
	print("+ python main.py -u USERNAME -p PASSWORD -o follow-tag -t TAG: Follow users using the tags you introduce")
	print("+ python main.py -u USERNAME -p PASSWORD -o follow-location -t LOCATION_ID: Follow users from a location")
	print("+ python main.py -u USERNAME -p PASSWORD -o follow-list -t USER_LIST: Follow users from a file")
	print("+ python main.py -u USERNAME -p PASSWORD -o super-followback: Follow back all the users who you dont follow back")
	print("+ python main.py -u USERNAME -p PASSWORD -o super-unfollow: Unfollow all the users who dont follow you back")
	print("+ python main.py -u USERNAME -p PASSWORD -o unfollow-all: Unfollow all the users")


def info():
	print("I follow them but they dont follow me:\n")
	tot = 0
	for i in followings:
		if i not in followers:
			tot=tot+1
			print(str(tot)+" "+i)
			with open("dont_follow_me.txt", "w") as text_file:
				text_file.write(str(tot)+" "+i)

	print("\nThey follow me but i dont follow them:\n")
	tot = 0
	for i in followers:
		if i not in followings:
			tot=tot+1
			print(str(tot)+" "+i)

	print("\nPeople following me:\n")
	tot = 0
	for i in followers:
		tot=tot+1
		print(str(tot)+" "+i)
	print("\nTotal: "+str(tot))

	print("\nPeople I follow:\n")
	tot = 0
	for i in followings:
		tot=tot+1
		print(str(tot)+" "+i)
	print("\nTotal: "+str(tot))

def follow_tag(tag):
	api.tagFeed(tag)
	media_id = api.LastJson
	tot = 0
	print("\nTAG: "+str(tag)+"\n")
	for i in media_id["items"]:
		time.sleep(float( random.uniform(min_delay*10,max_delay*10) / 10 ))
		username = i.get("user")["username"]
		user_id = i.get("user")["pk"]
		api.follow(user_id)
		tot += 1
		print("Following "+str(username)+" (with id "+str(user_id)+")")
		if(tot>=MAXIMO):
			break
	print("Total: "+str(tot)+" for tag "+tag+" (Max val: "+str(MAXIMO)+")\n")


def follow_location(target):
	api.getLocationFeed(target)
	media_id = api.LastJson
	tot = 0
	for i in media_id.get("items"):
		time.sleep(float( random.uniform(min_delay*10,max_delay*10) / 10 ))
		username = i.get("user").get("username")
		user_id = aux_funcs.get_id(username)
		api.follow(user_id)
		tot += 1
		print("Following "+str(username)+" (with id "+str(user_id)+")")
		if(tot>=MAXIMO):
			break
	print("Total: "+str(tot)+" for location "+str(target)+" (Max val: "+str(MAXIMO)+")\n")


def follow_list(target):
	user_list = open(target).read().splitlines()
	tot = 0
	for username in user_list:
		time.sleep(float( random.uniform(min_delay*10,max_delay*10) / 10 ))
		user_id = aux_funcs.get_id(username)
		api.follow(user_id)
		tot += 1
		print("Following "+str(username)+" (with id "+str(user_id)+")")
		if(tot>=MAXIMO):
			break
	print("Total: "+str(tot)+" users followed from "+str(target)+" (Max val: "+str(MAXIMO)+")\n")


def super_followback():
	count = 0
	for i in followers:
		if i not in followings:
			count+=1
			time.sleep(float( random.uniform(min_delay*10,max_delay*10) / 10 ))
			print(str(count)+") Following back "+i)
			user_id = aux_funcs.get_id(i)
			api.follow(user_id)


def super_unfollow():
	whitelist = open("whitelist.txt").read().splitlines()
	count = 0
	for i in followings:
		if (i not in followers) and (i not in whitelist):
			count+=1
			time.sleep(float( random.uniform(min_delay*10,max_delay*10) / 10 ))
			print(str(count)+") Unfollowing "+i)
			user_id = aux_funcs.get_id(i)
			api.unfollow(user_id)


def unfollowall():
	whitelist = open("whitelist.txt").read().splitlines()
	count = 0
	for i in followings:
		if i not in whitelist:
			count +=1
			time.sleep(float( random.uniform(min_delay*10,max_delay*10) / 10 ))
			print(str(count)+") Unfollowing "+i)
			user_id = aux_funcs.get_id(i)
			api.unfollow(user_id)


def start():
	API.login()
	for i in API.getTotalSelfFollowers():
		followers.append(i.get("username") )
	for i in API.getTotalSelfFollowings():
		followings.append(i.get("username") )
