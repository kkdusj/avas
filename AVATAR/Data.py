from config import API_ID, API_HASH, MONGO_DB_URL, user, dev, call, logger, logger_mode, botname, devname
from pymongo import MongoClient
from pyrogram import Client
from pytgcalls import PyTgCalls
from motor.motor_asyncio import AsyncIOMotorClient as _mongo_client_

mo = MongoClient()
mo = MongoClient(MONGO_DB_URL)
moo = mo["data"]
Bots = moo.Bots
bot_name = moo.bot_name
dev_name = moo.dev_name
botss = Bots
dev = {}
boot = {}

def dbb():
    global db
    db = {}

dbb()

# Developer Id
async def get_dev(bot_username):
  devv = dev.get(bot_username)
  if not devv:
   Bots = botss.find({})
   for i in Bots:
       bot = i["bot_username"]
       if bot == bot_username:
         devo = i["dev"]
         dev[bot_username] = devo
         return devo
  return devv


# Bot Name
async def get_bot_name(bot_username):
      name = botname.get(bot_username)
      if not name:
        bot = bot_name.find_one({"bot_username": bot_username})
        if not bot:
            return "avatar"
        botname[bot_username] = bot["bot_name"]
        return bot["bot_name"]
      return name

async def set_bot_name(bot_username: dict, BOT_NAME: str):
    botname[bot_username] = BOT_NAME
    bot_name.update_one({"bot_username": bot_username}, {"$set": {"bot_name": BOT_NAME}}, upsert=True)


async def get_dev_name(bot_username):
      name = devname.get(bot_username)
      if not name:
        dev = dev_name.find_one({"bot_username": bot_username})
        if not dev:
            return "كينج"
        devname[bot_username] = dev["dev_name"]
        return dev["dev_name"]
      return name

async def set_dev_name(bot_username: dict, DEV_NAME: str):
    devname[bot_username] = DEV_NAME
    dev_name.update_one({"bot_username": bot_username}, {"$set": {"dev_name": DEV_NAME}}, upsert=True)



#Mongo db
async def get_data(client):
   mongodb = _mongo_client_(MONGO_DB_URL)
   bot_username = client.me.username
   mongodb = mongodb[bot_username]
   return mongodb


# Assistant Client
async def get_userbot(bot_username):
  userbot = user.get(bot_username)
  if not userbot:
   Bots = botss.find({})
   for i in Bots:
       bot = i["bot_username"]
       if bot == bot_username:
         session = i["session"]
         userbot = Client("AVATAR", api_id=API_ID, api_hash=API_HASH, session_string=session)
         user[bot_username] = userbot
         return userbot
  return userbot

# Call Client
async def get_call(bot_username):
  calll = call.get(bot_username)
  if not calll:
   Bots = botss.find({})
   for i in Bots:
       bot = i["bot_username"]
       if bot == bot_username:
         userbot = await get_userbot(bot_username)
         callo = PyTgCalls(userbot, cache_duration=100)
         await callo.start()
         call[bot_username] = callo
         return callo
  return calll

# app Client
async def get_app(bot_username):
  app = boot.get(bot_username)
  if not app:
   Bots = botss.find({})
   for i in Bots:
       bot = i["bot_username"]
       if bot == bot_username:
         token = i["token"]
         app = Client("AVATAR", api_id=API_ID, api_hash=API_HASH, bot_token=token, plugins=dict(root="AVATAR"))
         boot[bot_username] = app
         return app
  return calll


# Logger
async def get_logger(bot_username):
  loggero = logger.get(bot_username)
  if not loggero:
   Bots = botss.find({})
   for i in Bots:
       bot = i["bot_username"]
       if bot == bot_username:
         loggero = i["logger"]
         logger[bot_username] = loggero
         return loggero
  return loggero


async def get_logger_mode(bot_username):
  logger = logger_mode.get(bot_username)
  if not logger:
   Bots = botss.find({})
   for i in Bots:
       bot = i["bot_username"]
       if bot == bot_username:
         logger = i["logger_mode"]
         logger_mode[bot_username] = logger
         return logger
  return logger
