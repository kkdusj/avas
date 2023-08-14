from pyrogram import Client, filters
from pyrogram import Client as app
from config import API_ID, API_HASH

bb = {}

@app.on_message(filters.command("نصب", ""))
async def hhu(app, message):
  ask = await app.ask(chat_id=message.chat.id, text="ارسل توكن البوت •", filters=filters.text)
  bot = Client(":memory:", api_id=API_ID, api_hash=API_HASH, bot_token=ask.text, in_memory=True, plugins=dict(root="El"))
  await bot.start()
  bb = bot

@app.on_message(filters.command("وقف", ""))
async def hhhu(app, message):
  await app.stop()

@Client.on_message(filters.command("/start", ""))
async def iaj(client, message):
  await message.reply_text("hi")
