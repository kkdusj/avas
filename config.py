## What's up Kangers
## Don't Kang without Creadits else I will rape your mom

import os
from os import getenv
from dotenv import load_dotenv

if os.path.exists("local.env"):
    load_dotenv("local.env")

load_dotenv()
admins = {}
user = {}
call = {}
dev = {}
logger = {}
logger_mode = {}
botname = {}
devname = {}
appp = {}
helper = {}

BOT_TOKEN = getenv("BOT_TOKEN", "5612068595:AAGWiiEE3jXB-AI2k08oYBS4EKgZA8j_VsM")
API_ID = int(getenv("API_ID", "13277434"))
API_HASH = getenv("API_HASH", "8444bed3061cda264cd6874de8fa45cc")
MONGO_DB_URL = getenv("MONGO_DB_URL", "mongodb+srv://45syaaa:45syaaa@avatar.hy1mnt3.mongodb.net/?retryWrites=true&w=majority")

