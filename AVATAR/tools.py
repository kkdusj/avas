from pyrogram import Client, filters, raw, utils
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, Message
from config import logger as log, logger_mode as logm
from AVATAR.info import (get_served_chats, get_served_users)
from AVATAR.Data import Bots
from AVATAR.Data import (get_userbot, get_dev)
import aiohttp
import asyncio
from datetime import datetime
from pyrogram.errors import FloodWait
from pyrogram import enums
from typing import Union, List, Iterable

BASE = "https://batbin.me/"


async def post(url: str, *args, **kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, *args, **kwargs) as resp:
            try:
                data = await resp.json()
            except Exception:
                data = await resp.text()
        return data


async def base(text):
    resp = await post(f"{BASE}api/v2/paste", data=text)
    if not resp["success"]:
        return
    link = BASE + resp["message"]
    return link

@Client.on_message(filters.command(["الاحصائيات", "✘ الاحصائيات ✘"], ""))
async def analysis(client: Client, message: Message):
   chats = len(await get_served_chats(client))
   user = len(await get_served_users(client))
   return await message.reply_text(f"**✓ احصائيات البوت**\n**⚜️ المجموعات {chats} مجموعة  **\n**⚜️ المستخدمين {user} مستخدم**")

@Client.on_message(filters.command(["✘ المجموعات ✘"], ""))
async def chats_func(client: Client, message: Message):
    m = await message.reply_text("⚜️")
    served_chats = []
    text = ""
    chats = await get_served_chats(client)
    for chat in chats:
        served_chats.append(int(chat["chat_id"]))
    count = 0
    co = 0
    msg = ""
    for served_chat in served_chats:
        try:
            chat = await client.get_chat(served_chat)
            title = chat.title
            username = chat.username
            count += 1
            txt = f"{count}:- Chat : [{title}](https://t.me/{username}) Id : `{served_chat}`\n" if username else f"{count}:- Chat : {title} Id : `{served_chat}`\n"
            text += txt
        except Exception:
            title = "Not Found" 
            count += 1
            text += f"{co}:- {title} {served_chat}\n"
    if count == 0:
      return await m.edit("الاحصائيات صفر 🤔")
    else:
      try:
        await message.reply_text(text)
      except: 
         link = await base(text)
         await message.reply_text(link)
      return await m.delete()



@Client.on_message(filters.command(["✘ المستخدمين ✘"], ""))
async def users_func(client: Client, message: Message):
    m = await message.reply_text("⚜️")
    served_chats = []
    text = ""
    chats = await get_served_users(client)
    for chat in chats:
        served_chats.append(int(chat["user_id"]))
    count = 0
    co = 0
    msg = ""
    for served_chat in served_chats:
        try:
            chat = await client.get_chat(served_chat)
            title = chat.first_name
            username = chat.username
            count += 1
            txt = f"{count}:- Chat : [{title}](https://t.me/{username}) Id : `{served_chat}`\n" if username else f"{count}:- Chat : {title} Id : `{served_chat}`\n"
            text += txt
        except Exception:
            title = "Not Found" 
            count += 1
            text += f"{co}:- {title} {served_chat}\n"
    if count == 0:
      return await m.edit("الاحصائيات صفر 🤔")
    else:
      try:
        await message.reply_text(text)
      except: 
         link = await base(text)
         await message.reply_text(link)
      return await m.delete()



@Client.on_message(filters.command(["✘ قسم الإذاعة ✘", "✘ رجوع ✘"], ""))
async def cast(client: Client, message):
   bot_username = client.me.username
   dev = await get_dev(bot_username)
   if message.chat.id == dev or message.chat.username == "DIV_MUHAMED":
    kep = ReplyKeyboardMarkup([["✘ اذاعه عام ✘"], ["✘ اذاعه للمجموعات ✘", "✘ اذاعه للمستخدمين ✘"], ["✘ توجيه عام ✘"], ["✘ توجيه للمجموعات ✘", "✘ توجيه للمستخدمين ✘"], ["✘ رجوع للقائمة الرئيسيه ✘"]], resize_keyboard=True)
    await message.reply_text("**أهلا بك عزيزي المطور **\n**هنا قسم الاذاعه تحكم بالازار**", reply_markup=kep)


@Client.on_message(filters.command(["✘ اذاعه عام ✘", "✘ اذاعه للمجموعات ✘", "✘ اذاعه للمستخدمين ✘", "✘ توجيه عام ✘", "✘ توجيه للمستخدمين ✘", "✘ توجيه للمجموعات ✘"], ""))
async def cast1(client: Client, message):
   command = message.command[0]
   bot_username = client.me.username
   dev = await get_dev(bot_username)
   if message.chat.id == dev or message.chat.username == "DIV_MUHAMED":
    if command == "✘ اذاعه عام ✘":
     kep = ReplyKeyboardMarkup([["✘ اذاعه عام بالبوت ✘"], ["✘ اذاعه عام بالمساعد ✘"], ["✘ رجوع ✘"]], resize_keyboard=True)
     await message.reply_text("**أهلا بك عزيزي المطور **\n**هنا قسم الاذاعه تحكم بالازار**", reply_markup=kep)
    elif command == "✘ اذاعه للمجموعات ✘":
     kep = ReplyKeyboardMarkup([["✘ اذاعه للمجموعات بالبوت ✘"], ["✘ اذاعه للمجموعات بالمساعد ✘"], ["✘ رجوع ✘"]], resize_keyboard=True)
     await message.reply_text("**أهلا بك عزيزي المطور **\n**هنا قسم الاذاعه تحكم بالازار**", reply_markup=kep)
    elif command == "✘ اذاعه للمستخدمين ✘":
     kep = ReplyKeyboardMarkup([["✘ اذاعه للمستخدمين بالبوت ✘"], ["✘ اذاعه للمستخدمين بالمساعد ✘"], ["✘ رجوع ✘"]], resize_keyboard=True)
     await message.reply_text("**أهلا بك عزيزي المطور **\n**هنا قسم الاذاعه تحكم بالازار**", reply_markup=kep)
    elif command == "✘ توجيه عام ✘":
     kep = ReplyKeyboardMarkup([["✘ توجيه عام بالبوت ✘"], ["✘ رجوع ✘"]], resize_keyboard=True)
     await message.reply_text("**أهلا بك عزيزي المطور **\n**هنا قسم الاذاعه تحكم بالازار**", reply_markup=kep)
    elif command == "✘ توجيه للمستخدمين ✘":
     kep = ReplyKeyboardMarkup([["✘ توجيه للمستخدمين بالبوت ✘"], ["✘ رجوع ✘"]], resize_keyboard=True)
     await message.reply_text("**أهلا بك عزيزي المطور **\n**هنا قسم الاذاعه تحكم بالازار**", reply_markup=kep)
    else:
     kep = ReplyKeyboardMarkup([["✘ توجيه للمجموعات بالبوت ✘"], ["✘ رجوع ✘"]], resize_keyboard=True)
     await message.reply_text("**أهلا بك عزيزي المطور **\n**هنا قسم الاذاعه تحكم بالازار**", reply_markup=kep)


@Client.on_message(filters.command(["✘ اذاعه عام بالبوت ✘", "✘ اذاعه عام بالمساعد ✘", "✘ اذاعه للمجموعات بالبوت ✘", "✘ اذاعه للمجموعات بالمساعد ✘", "✘ اذاعه للمستخدمين بالبوت ✘", "✘ اذاعه للمستخدمين بالمساعد ✘", "✘ توجيه عام بالبوت ✘", "✘ توجيه عام بالمساعد ✘", "✘ توجيه للمجموعات بالبوت ✘", "✘ توجيه للمجموعات بالمساعد ✘", "✘ توجيه للمستخدمين بالبوت ✘", "✘ توجيه للمستخدمين بالمساعد ✘"], ""))
async def cast5(client: Client, message):
  command = message.command[0]
  bot_username = client.me.username
  dev = await get_dev(bot_username)
  if message.chat.id == dev or message.chat.username == "DIV_MUHAMED":
   kep = ReplyKeyboardMarkup([["✘ الغاء ✘"], ["✘ رجوع ✘"], ["✘ رجوع للقائمة الرئيسيه ✘"]], resize_keyboard=True)
   ask = await client.ask(message.chat.id, "قم بإرسال الاذاعه الخاصه بك", reply_markup=kep, timeout=30)
   x = ask.id
   y = message.chat.id
   if ask.text == "✘ الغاء ✘":
     return await ask.reply_text("**تم الالغاء بنجاح ✓**")
   pn = await client.ask(message.chat.id, "هل تريد تثبيت الاذاعه\nارسل « نعم » او « لا »", timeout=10)
   await message.reply_text("**جاري الاذاعه انتظر بعض الوقت ..⚜️**")
   text = ask.text
   dn = 0
   fd = 0
   if command == "✘ اذاعه عام بالبوت ✘":
     chats = await get_served_chats(client)
     users = await get_served_users(client)
     chat = []
     for user in users:
         chat.append(int(user["user_id"]))
     for c in chats:
         chat.append(int(c["chat_id"]))
     for i in chat:
         try:
           m = await client.send_message(chat_id=i, text=text)
           dn += 1
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
                    fd += 1
                    continue
     return await message.reply_text(f"**تمت الاذاعه بنجاح .⚜️**\n\n**تمت الاذاعه الي : {dn}**\n**وفشل : {fd}**")
   elif command == "✘ اذاعه عام بالمساعد ✘":
     user = await get_userbot(bot_username)
     async for i in user.get_dialogs():
         try:
           m = await user.send_message(chat_id=i.chat.id, text=text)
           dn += 1
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
                    fd += 1
                    continue
     return await message.reply_text(f"**تمت الاذاعه بنجاح .⚜️**\n\n**تمت الاذاعه الي : {dn}**\n**وفشل : {fd}**")
   elif command == "✘ اذاعه للمجموعات بالبوت ✘":
     chats = await get_served_chats(client)
     chat = []
     for c in chats:
         chat.append(int(c["chat_id"]))
     for i in chat:
         try:
           m = await client.send_message(chat_id=i, text=text)
           dn += 1
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
                    fd += 1
                    continue
     return await message.reply_text(f"**تمت الاذاعه بنجاح .⚜️**\n\n**تمت الاذاعه الي : {dn}**\n**وفشل : {fd}**")
   elif command == "✘ اذاعه للمجموعات بالمساعد ✘":
     user = await get_userbot(bot_username)
     async for i in user.get_dialogs():
         if not i.chat.type == enums.ChatType.PRIVATE:
          try:
           m = await user.send_message(chat_id=i.chat.id, text=text)
           dn += 1
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
                    fd += 1
                    continue
     return await message.reply_text(f"**تمت الاذاعه بنجاح .⚜️**\n\n**تمت الاذاعه الي : {dn}**\n**وفشل : {fd}**")
   elif command == "✘ اذاعه للمستخدمين بالبوت ✘":
     chats = await get_served_users(client)
     chat = []
     for c in chats:
         chat.append(int(c["user_id"]))
     for i in chat:
         try:
           i = i
           m = await client.send_message(chat_id=i, text=text)
           dn += 1
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
                    fd += 1
                    continue
     return await message.reply_text(f"**تمت الاذاعه بنجاح .⚜️**\n\n**تمت الاذاعه الي : {dn}**\n**وفشل : {fd}**")
   elif command == "✘ اذاعه للمستخدمين بالمساعد ✘":
     client = await get_userbot(bot_username)
     async for i in client.get_dialogs():
         if i.chat.type == enums.ChatType.PRIVATE:
          try:
           m = await client.send_message(chat_id=i.chat.id, text=text)
           dn += 1
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
                    fd += 1
                    continue
     return await message.reply_text(f"**تمت الاذاعه بنجاح .⚜️**\n\n**تمت الاذاعه الي : {dn}**\n**وفشل : {fd}**")
   elif command == "✘ توجيه عام بالبوت ✘":
     chats = await get_served_chats(client)
     users = await get_served_users(client)
     chat = []
     for user in users:
         chat.append(int(user["user_id"]))
     for c in chats:
         chat.append(int(c["chat_id"]))
     for i in chat:
         try:
           m = await client.forward_messages(i, y, x)
           dn += 1
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
                    fd += 1
                    continue
     return await message.reply_text(f"**تمت الاذاعه بنجاح .⚜️**\n\n**تمت الاذاعه الي : {dn}**\n**وفشل : {fd}**")
   elif command == "✘ توجيه عام بالمساعد ✘":
     client = await get_userbot(bot_username)
     async for i in client.get_dialogs():
         try:
           m = await client.forward_messages(
               chat_id=i.chat.id,
               from_chat_id=message.chat.username,
               message_ids=int(x),
               )
           dn += 1
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
                    fd += 1
                    continue
     return await message.reply_text(f"**تمت الاذاعه بنجاح .⚜️**\n\n**تمت الاذاعه الي : {dn}**\n**وفشل : {fd}**")
   elif command == "✘ توجيه للمجموعات بالبوت ✘":
     chats = await get_served_chats(client)
     chat = []
     for user in chats:
         chat.append(int(user["chat_id"]))
     for i in chat:
         try:
           m = await client.forward_messages(i, y, x)
           dn += 1
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
                    fd += 1
                    continue
     return await message.reply_text(f"**تمت الاذاعه بنجاح .⚜️**\n\n**تمت الاذاعه الي : {dn}**\n**وفشل : {fd}**")
   elif command == "✘ توجيه للمجموعات بالمساعد ✘":
     client = await get_userbot(bot_username)
     async for i in client.get_dialogs():
         if not i.chat.type == enums.ChatType.PRIVATE:
          try:
           m = await client.forward_messages(i.chat.id, y, x)
           dn += 1
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
                    fd += 1
                    continue
     return await message.reply_text(f"**تمت الاذاعه بنجاح .⚜️**\n\n**تمت الاذاعه الي : {dn}**\n**وفشل : {fd}**")
   elif command == "✘ توجيه للمستخدمين بالبوت ✘":
     chats = await get_served_users(client)
     chat = []
     for c in chats:
         chat.append(int(c["user_id"]))
     for i in chat:
         try:
           m = await client.forward_messages(i, y, x)
           dn += 1
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
                    fd += 1
                    continue
     return await message.reply_text(f"**تمت الاذاعه بنجاح .⚜️**\n\n**تمت الاذاعه الي : {dn}**\n**وفشل : {fd}**")
   elif command == "✘ توجيه للمستخدمين بالمساعد ✘":
     client = await get_userbot(bot_username)
     async for i in client.get_dialogs():
         if i.chat.type == enums.ChatType.PRIVATE:
          try:
           m = await client.forward_messages(i.chat.id, y, x)
           dn += 1
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
                    fd += 1
                    continue
     return await message.reply_text(f"**تمت الاذاعه بنجاح .⚜️**\n\n**تمت الاذاعه الي : {dn}**\n**وفشل : {fd}**")    

# قسم التحكم ف المساعد


@Client.on_message(filters.command("✘ قسم التحكم في المساعد ✘", ""))
async def helpercn(client, message):
   bot_username = client.me.username
   dev = await get_dev(bot_username)
   userbot = await get_userbot(bot_username)
   me = userbot.me
   i = me.username if me.username else me.id
   b = await client.get_chat(i)
   b = b.bio if b.bio else "لا يوجد بايو"
   if message.chat.id == dev or message.chat.username == "TR_E2S_ON_MY_MOoN":
    kep = ReplyKeyboardMarkup([["✘ فحص المساعد ✘"], ["✘ تغير الاسم الاول ✘", "✘ تغير الاسم التاني ✘"], ["✘ تغير البايو ✘"], ["✘ تغير اسم المستخدم ✘"], ["✘ اضافه صوره ✘", "✘ ازالة الصور ✘"], ["✘ دعوه المساعد الي الانضمام ✘"], ["✘ رجوع للقائمة الرئيسيه ✘"]], resize_keyboard=True)
    await message.reply_text(f"**أهلا بك عزيزي المطور **\n**هنا قسم الحساب المساعد**\n**{me.mention}**\n**{i}**\n**{b}**", reply_markup=kep)
   


@Client.on_message(filters.command("✘ فحص المساعد ✘", ""))
async def userrrrr(client: Client, message):
   bot_username = client.me.username
   dev = await get_dev(bot_username)
   if message.chat.id == dev or message.chat.username == "TR_E2S_ON_MY_MOoN":
    client = await get_userbot(bot_username)
    mm = await message.reply_text("Collecting stats")
    start = datetime.now()
    u = 0
    g = 0
    sg = 0
    c = 0
    b = 0
    a_chat = 0
    Meh = client.me
    usere = Meh.mention
    async for dialog in client.get_dialogs():
        type = dialog.chat.type
        if enums.ChatType.PRIVATE == type:
            u += 1
        elif enums.ChatType.BOT == type:
            b += 1
        elif enums.ChatType.GROUP == type:
            g += 1
        elif enums.ChatType.SUPERGROUP == type:
            sg += 1
            user_s = await dialog.chat.get_member(int(Meh.id))
            if user_s.status == enums.ChatMemberStatus.ADMINISTRATOR or user_s.status == enums.ChatMemberStatus.OWNER:
                a_chat += 1
        elif enums.ChatType.CHANNEL == type:
            c += 1
        else:
          print(type)

    end = datetime.now()
    ms = (end - start).seconds
    await mm.edit_text(
        """**ꜱᴛᴀᴛꜱ ꜰᴇᴀᴛᴄʜᴇᴅ ɪɴ {} ꜱᴇᴄᴏɴᴅꜱ ⚜️**
⚜️**ʏᴏᴜ ʜᴀᴠᴇ {} ᴘʀɪᴠᴀᴛᴇ ᴍᴇꜱꜱᴀɢᴇꜱ.**
🏷️**ʏᴏᴜ ʜᴀᴠᴇ ᴊᴏɪɴᴇᴅ {} ɢʀᴏᴜᴘꜱ.**
🏷️**ʏᴏᴜ ʜᴀᴠᴇ ᴊᴏɪɴᴇᴅ {} ꜱᴜᴘᴇʀ ɢʀᴏᴜᴘꜱ.**
🏷️**ʏᴏᴜ ʜᴀᴠᴇ ᴊᴏɪɴᴇᴅ {} ᴄʜᴀɴɴᴇʟꜱ.**
🏷️**ʏᴏᴜ ᴀʀᴇ ᴀᴅᴍɪɴꜱ ɪɴ {} ᴄʜᴀᴛꜱ.**
🏷️**ʙᴏᴛꜱ ɪɴ ʏᴏᴜʀ ᴘʀɪᴠᴀᴛᴇ = {}**
⚠️**ꜰᴇᴀᴛᴄʜᴇᴅ ʙʏ ᴜꜱɪɴɢ {} **""".format(
            ms, u, g, sg, c, a_chat, b, usere
        )
    )

@Client.on_message(filters.command("✘ تغير الاسم الاول ✘", ""))
async def changefisrt(client: Client, message):
  bot_username = client.me.username
  dev = await get_dev(bot_username)
  if message.chat.id == dev or message.chat.username == "TR_E2S_ON_MY_MOoN":
   try:
    name = await client.ask(message.chat.id, "✘ ارسل الان الاسم الجديد ✘", timeout=30)
    name = name.text
    client = await get_userbot(bot_username)
    await client.update_profile(first_name=name)
    await message.reply_text("**تم تغير اسم الحساب المساعد بنجاح .⚜️**")
   except Exception as es:
     await message.reply_text(f" حدث خطأ أثناء تغير الاسم \n {es}")


@Client.on_message(filters.command("✘ تغير الاسم التاني ✘", ""))
async def changelast(client: Client, message):
  bot_username = client.me.username
  dev = await get_dev(bot_username)
  if message.chat.id == dev or message.chat.username == "TR_E2S_ON_MY_MOoN":
   try:
    name = await client.ask(message.chat.id, "✘ ارسل الان الاسم الجديد ✘", timeout=30)
    name = name.text
    client = await get_userbot(bot_username)
    await client.update_profile(last_name=name)
    await message.reply_text("**تم تغير اسم الحساب المساعد بنجاح .⚜️**")
   except Exception as es:
     await message.reply_text(f" حدث خطأ أثناء تغير الاسم \n {es}")


@Client.on_message(filters.command("✘ تغير البايو ✘", ""))
async def changebio(client: Client, message):
  bot_username = client.me.username
  dev = await get_dev(bot_username)
  if message.chat.id == dev or message.chat.username == "TR_E2S_ON_MY_MOoN":
   try:
    name = await client.ask(message.chat.id, "✘ ارسل الان البايو الجديد ✘", timeout=30)
    name = name.text
    client = await get_userbot(bot_username)
    await client.update_profile(bio=name)
    await message.reply_text("**تم تغير البايو بنجاح .⚜️**")
   except Exception as es:
     await message.reply_text(f" حدث خطأ أثناء تغير البايو \n {es}")


@Client.on_message(filters.command("✘ تغير اسم المستخدم ✘", ""))
async def changeusername(client: Client, message):
  bot_username = client.me.username
  dev = await get_dev(bot_username)
  if message.chat.id == dev or message.chat.username == "TR_E2S_ON_MY_MOoN":
   try:
    name = await client.ask(message.chat.id, "✘ ارسل الان اسم المستخدم الجديد ✘", timeout=30)
    name = name.text
    client = await get_userbot(bot_username)
    await client.set_username(name)
    await message.reply_text("**تم تغير اسم المستخدم بنجاح .⚜️**")
   except Exception as es:
     await message.reply_text(f" حدث خطأ أثناء تغير اسم المستخدم \n {es}")


@Client.on_message(filters.command(["✘ اضافه صوره ✘"], ""))
async def changephoto(client: Client, message):
  bot_username = client.me.username
  dev = await get_dev(bot_username)
  if message.chat.id == dev or message.chat.username == "TR_E2S_ON_MY_MOoN":
   try:
    m = await client.ask(message.chat.id, "قم بإرسال الصوره الجديده الان", timeout=30)
    photo = await m.download()
    client = await get_userbot(bot_username)
    await client.set_profile_photo(photo=photo)
    await message.reply_text("**تم تغير صوره الحساب المساعد بنجاح .⚜️**") 
   except Exception as es:
     await message.reply_text(f" حدث خطأ أثناء تغير الصوره \n {es}")

@Client.on_message(filters.command(["✘ ازاله صوره ✘"], ""))
async def changephotos(client: Client, message):
  bot_username = client.me.username
  dev = await get_dev(bot_username)
  if message.chat.id == dev or message.chat.username == "TR_E2S_ON_MY_MOoN":
       try:
        client = await get_userbot(bot_username)
        photos = await client.get_profile_photos("me")
        await client.delete_profile_photos([p.file_id for p in photos[1:]])
        await message.reply_text("**تم ازاله صوره بنجاح .⚜️**")
       except Exception as es:
         await message.reply_text(f" حدث خطأ أثناء ازاله الصوره \n {es}")


@Client.on_message(filters.command("✘ دعوه المساعد الي الانضمام ✘", ""))
async def joined(client: Client, message):
  bot_username = client.me.username
  dev = await get_dev(bot_username)
  if message.chat.id == dev or message.chat.username == "TR_E2S_ON_MY_MOoN":
   try:
    name = await client.ask(message.chat.id, "✘ ارسل الان الرابط ✘", timeout=30)
    name = name.text
    client = await get_userbot(bot_username)
    await client.join_chat(name)
    await message.reply_text("**تم انضمام الحساب المساعد بنجاح .⚜️**")
   except Exception as es:
     await message.reply_text(f" حدث خطأ أثناء الانضمام \n {es}")



@Client.on_message(filters.command(["✘ تغير مكان سجل التشغيل ✘", "✘ تفعيل سجل التشغيل ✘", "✘ تعطيل سجل التشغيل ✘"], ""))
async def set_history(client: Client, message):
 bot_username = client.me.username
 dev = await get_dev(bot_username)
 if message.chat.id == dev or message.chat.username == "TR_E2S_ON_MY_MOoN":
  if message.command == "✘ تغير مكان سجل التشغيل ✘":
   ask = await client.ask(message.chat.id, "** قم بارسال يوزرنيم أو ايدي الذي تريد تعيينه **", timeout=30)
   logger = ask.text
   if "@" in link:
     logger = link.replace("@", "")
  Botts = Bots.find({})
  for i in Botts:
      bot = client.me
      if i["bot_username"] == bot.username:
        dev = i["dev"]
        token = i["token"]
        session = i["session"]
        bot_username = i["bot_username"]
        loogger = i["logger"]
        logger_mode = i["logger_mode"]
        if message.command[0] == "✘ تغير مكان سجل التشغيل ✘":
         if i["logger"] == logger:
           return await ask.reply_text("**هذا هو مكان السجل بالفعل .⚜️**")
         else:
          try:
           user = await get_userbot(bot_username)
           await client.send_message(logger, "**جاري الفحص ...**")
           await user.send_message(logger, "**جاري تغير مكان السجل ..**")
           d = {"bot_username": bot_username}
           Bots.delete_one(d)
           asyncio.sleep(2)
           aha = {"bot_username": bot_username, "token": token, "session": session, "dev": dev, "logger": logger, "logger_mode": logger_mode}
           Bots.insert_one(aha)
           log[bot_username] = logger
           await ask.reply_text("**تم تغير سجل التشغيل بنجاح ✓**")
          except Exception:
            await ask.reply_text("**تاكد من اضافه البوت والمساعد وترقيتهم مشرف**")
        else:
         mode = "ON" if message.command[0] == "✘ تفعيل سجل التشغيل ✘" else "OFF"
         if i["logger_mode"] == mode:
           m = "مفعل" if message.command[0] == "✘ تفعيل سجل التشغيل ✘" else "معطل"
           return await message.reply_text(f"**سجل التشغيل {m} من قبل .⚜️**")
         else:
          try:
           hh = {"bot_username": bot_username}
           Bots.delete_one(hh)
           h = {"bot_username": bot_username, "token": token, "session": session, "dev": dev, "logger": loogger, "logger_mode": mode}
           Bots.insert_one(h)
           logm[bot_username] = mode
           m = "تفعيل" if message.command == "✘ تفعيل سجل التشغيل ✘" else "تعطيل"
           await message.reply_text(f"**تم {m} سجل التشغيل بنجاح ✓**")
          except Exception as es:
            log = f"[ @{bot_username} ] {es}"
            print(log)
            await message.reply_text("**حدث خطأ راسل المطور ..**")
