from pyrogram import Client, filters
from youtubesearchpython.__future__ import VideosSearch 
import os
import aiohttp
import requests
import random 
import asyncio
import yt_dlp
from datetime import datetime, timedelta
from youtube_search import YoutubeSearch
from pytgcalls.types.input_stream.quality import (HighQualityAudio,
                                                  HighQualityVideo,
                                                  LowQualityAudio,
                                                  LowQualityVideo,
                                                  MediumQualityAudio,
                                                  MediumQualityVideo)
from AVATAR.info import (get_served_chats, get_served_users)
from AVATAR.Data import Bots
from AVATAR.Data import (get_userbot, get_dev)                                                  
from typing import Union
from pyrogram import Client, filters 
from pyrogram import Client as client
from pyrogram.errors import (ChatAdminRequired,
                             UserAlreadyParticipant,
                             UserNotParticipant)
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatType, ChatMemberStatus
from pytgcalls import PyTgCalls, StreamType
from pytgcalls.exceptions import (AlreadyJoinedError,
                                  NoActiveGroupCall,
                                  TelegramServerError)
from pytgcalls.types import (JoinedGroupCallParticipant,
                             LeftGroupCallParticipant, Update)
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.stream import StreamAudioEnded
from config import API_ID, API_HASH, MONGO_DB_URL
from motor.motor_asyncio import AsyncIOMotorClient as _mongo_client_
from pymongo import MongoClient
from AVATAR.info import (db, add, is_served_call, add_active_video_chat, add_served_call, add_active_chat, gen_thumb, download, remove_active)
from AVATAR.Data import (get_logger, get_userbot, get_call, get_logger_mode)
import asyncio
             
mongodb = _mongo_client_(MONGO_DB_URL)
pymongodb = MongoClient(MONGO_DB_URL)
Bots = pymongodb.Bots


async def join_assistant(client, chat_id, message_id, userbot, file_path):
        join = None
        try:
            try:
                user = userbot.me
                user_id = user.id
                get = await client.get_chat_member(chat_id, user_id)
            except ChatAdminRequired:
                await client.send_message(chat_id, f"**قم بترقية البوت مشرف .⚜️**", reply_to_message_id=message_id)
            if get.status == ChatMemberStatus.BANNED:
                await client.send_message(chat_id, f"**قم بالغاء الحظر عن الحساب المساعد لتفعيل البوت**.\n\n @{user.username} : **الحساب المساعد **⚜️.\n** قم بتنظيف قايمه المستدخمين تمت ازالتهم ⚜️.**\n\n** @swad_source : او تواصل مع المطور من هنا ⚜️.**", reply_to_message_id=message_id)
            else:
              join = True
        except UserNotParticipant:
            chat = await client.get_chat(chat_id)
            if chat.username:
                try:
                    await userbot.join_chat(chat.username)
                    join = True
                except UserAlreadyParticipant:
                    join = True
                except Exception:
                 try:
                  invitelink = (await client.export_chat_invite_link(chat_id))
                  if invitelink.startswith("https://t.me/+"):
                        invitelink = invitelink.replace("https://t.me/+", "https://t.me/joinchat/")
                  await asyncio.sleep(3)
                  await userbot.join_chat(invitelink)
                  join = True
                 except ChatAdminRequired:
                    return await client.send_message(chat_id, f"**قم اعطاء البوت صلاحيه اضافه المستخدمين عبر الرابط .⚜️**", reply_to_message_id=message_id)
                 except Exception as e:
                   await client.send_message(chat_id, "** حدث خطأ حاول مرا آخري لاحقا**\n** @swad_source : او تواصل مع الدعم من هنا .⚜️**", reply_to_message_id=message_id)
            else:
                try:
                    try:
                       invitelink = chat.invite_link
                       if invitelink is None:
                          invitelink = (await client.export_chat_invite_link(chat_id))
                    except Exception:
                        try:
                          invitelink = (await client.export_chat_invite_link(chat_id))
                        except ChatAdminRequired:
                          await client.send_message(chat_id, f"**قم اعطاء البوت صلاحيه اضافه مستخدمين عبر الرابط .⚜️**", reply_to_message_id=message_id)
                        except Exception as e:
                          await client.send_message(chat_id, "** حدث خطأ حاول مرا آخري لاحقا**\n** @swad_source : او تواصل مع الدعم من هنا .⚜️**", reply_to_message_id=message_id)
                    m = await client.send_message(chat_id, "**انتظر قليلاً جاري تفعيل البوت .⚜️**")
                    if invitelink.startswith("https://t.me/+"):
                        invitelink = invitelink.replace("https://t.me/+", "https://t.me/joinchat/")
                    await userbot.join_chat(invitelink)
                    join = True
                    await m.edit(f"**{user.mention} : انضم الحساب المساعد **\n**وتم تفعيل البوت يمكنك التشغيل الان .⚜️**")
                except UserAlreadyParticipant:
                    join = True
                except Exception as e:
                    await client.send_message(chat_id, "** حدث خطأ حاول مرا آخري لاحقا**\n** @swad_source : او تواصل مع الدعم من هنا .⚜️**", reply_to_message_id=message_id)
        return join        

async def join_call(
        client,
        message_id,
        chat_id,
        bot_username,
        file_path,
        link,
        vid: Union[bool, str] = None):
        userbot = await get_userbot(bot_username)
        Done = None
        try:
          call = await get_call(bot_username)
        except:
          try:
            os.remove(file_path)
          except:
            pass
          return Done
        if link:
          file_path = await download(link, vid)
        else:
          file_path = file_path
        audio_stream_quality = MediumQualityAudio()
        video_stream_quality = MediumQualityVideo()
        stream = (AudioVideoPiped(file_path, audio_parameters=audio_stream_quality, video_parameters=video_stream_quality) if vid else AudioPiped(file_path, audio_parameters=audio_stream_quality))
        try:
            await call.join_group_call(chat_id, stream, stream_type=StreamType().pulse_stream)
            Done = True
        except NoActiveGroupCall:
                 h = await join_assistant(client, chat_id, message_id, userbot, file_path)
                 if h:
                  try:
                   await call.join_group_call(chat_id, stream, stream_type=StreamType().pulse_stream)
                   Done = True
                  except Exception:
                      await client.send_message(chat_id, "**قم بتشغيل المكالمة أولاً .🔥**", reply_to_message_id=message_id)
        except AlreadyJoinedError:
             await client.send_message(chat_id, "**قم بإعادة تشغيل المكالمة ..🔥**", reply_to_message_id=message_id)
        except TelegramServerError:
             await client.send_message(chat_id, "**قم بإعادة تشغيل المكالمة ..🔥**", reply_to_message_id=message_id)
        try:
          os.remove(file_path)
        except:
          pass
        return Done


def seconds_to_min(seconds):
    if seconds is not None:
        seconds = int(seconds)
        d, h, m, s = (
            seconds // (3600 * 24),
            seconds // 3600 % 24,
            seconds % 3600 // 60,
            seconds % 3600 % 60,
        )
        if d > 0:
            return "{:02d}:{:02d}:{:02d}:{:02d}".format(d, h, m, s)
        elif h > 0:
            return "{:02d}:{:02d}:{:02d}".format(h, m, s)
        elif m > 0:
            return "{:02d}:{:02d}".format(m, s)
        elif s > 0:
            return "00:{:02d}".format(s)
    return "-"


async def logs(bot_username, client, message):
   if await get_logger_mode(bot_username) == "OFF":
     return
   logger = await get_logger(bot_username)
   if message.chat.type == "channel":
     chat = f"[{message.chat.title}](t.me/{message.chat.username})" if message.chat.username else message.chat.title
     name = f"[{message.chat.title}](https://t.me/{message.chat.username})" if message.chat.username else f"{message.chat.title}"
     name = f"{message.author_signature}" if message.author_signature else chatname
     text = f"**Playing History . **\n\n**Chat : {chat}**\n**Chat Id : {message.chat.id}**\n**User Name : {name}**\n\n**Played : {message.text}**"
   else:
     chat = f"[{message.chat.title}](t.me/{message.chat.username})" if message.chat.username else message.chat.title
     user = f"User Username : @{message.from_user.username}" if message.from_user.username else f"User Id : {message.from_user.id}"
     text = f"**Playing History **\n\n**Chat : {chat}**\n**Chat Id : {message.chat.id}**\n**User Name : {message.from_user.mention}**\n**{user}**\n\n**Played : {message.text}**"
   return await client.send_message(logger, text=text, disable_web_page_preview=True)



@Client.on_message(filters.regex("^مين في الكول$|^مين ف الكول$|^مين في كول$"))
async def strcall(client: Client, message):
    assistant = await join_assistant(message.chat.id)
    try:
        await assistant.join_group_call(message.chat.id, AudioPiped("./AVATAR/dd.mp3"), stream_type=StreamType().pulse_stream)
        text="الاعضاء المتواجدين فالمكالمه\n\n"
        participants = await assistant.get_participants(message.chat.id)
        k =0
        for participant in participants:
            info = participant
            if info.muted == False:
                mut=f" يتحدث • \n"
            else:
                mut=" صامت • \n"
            user = await client.get_users(participant.user_id)
            print(participant.user_id)
            k +=1
            text +=f"{k}»» {user.mention}{mut}\n"   
        await message.reply(f"{text}")
        await asyncio.sleep(5)
        await assistant.leave_group_call(message.chat.id)
    except NoActiveGroupCall:
        await message.reply(f"قلبي المكالمه غير مفتوحه")
    except AlreadyJoinedError:
        text="الاعضاء المتواجدين فالمكالمه\n\n"
        participants = await assistant.get_participants(message.chat.id)
        k =0
        for participant in participants:
            info = participant
            if info.muted == False:
                mut=f" • يتحدث\n"
            else:
                mut=" صامت • \n"
            user = await client.get_users(participant.user_id)
            print(participant.user_id)
            k +=1
            text +=f"{k}»» {user.mention}{mut}\n"
        await message.reply(f"{text}")
    except TelegramServerError:
        await message.reply(f"يوجد مشكله ارسل الامر ثانيا")
        
        




@Client.on_message(filters.command(["عشوائي", "تشغيل عشوائي"], ""))
async def aii(client: Client, message):
   try:
    rep = await message.reply_text("**جاري اختيار تشغيل عشوائي ..🔥**")
    message_id = message.id
    chat_id = message.chat.id
    bot_username = client.me.username
    user = await get_userbot(bot_username)
    req = message.from_user.mention if message.from_user else message.chat.title
    raw_list = []
    async for msg in user.get_chat_history("avatarmusic1"):
        if msg.audio:
          raw_list.append(msg)
    x = random.choice(raw_list)
    file_path = await x.download()
    file_name = x.audio.title
    title = file_name
    dur = x.audio.duration
    duration = seconds_to_min(dur)
    photo = "https://graph.org/file/9cdbc1531679dc7a507f8.jpg"
    vid = True if x.video else None
    chat_id = message.chat.id
    user_id = message.from_user.id if message.from_user else "TR_E2S_ON_MY_MOoN"
    videoid = None
    link = None
    await add(message.chat.id, bot_username, file_path, link, title, duration, videoid, vid, user_id)
    if not await is_served_call(client, message.chat.id): 
      await add_active_chat(chat_id)
      await add_served_call(client, chat_id)
      if vid:
        await add_active_video_chat(chat_id)
      link = None
      c = await join_call(client, message_id, chat_id, bot_username, file_path, link, vid)
      if not c:
            await remove_active(bot_username, chat_id)
            return await rep.delete()
    await rep.delete()
    button = [[InlineKeyboardButton(text="END", callback_data=f"stop"), InlineKeyboardButton(text="RESUME", callback_data=f"resume"), InlineKeyboardButton(text="PAUSE", callback_data=f"pause")], [InlineKeyboardButton(text="᥉᥆υᖇᥴᥱ✘", url="https://t.me/sourceav"), InlineKeyboardButton(text="GᖇOᑌᑭ✘", url="https://t.me/va_source")], [InlineKeyboardButton(text="₍ 𝑘 𝑖 𝑛 𝑔 || كـ ٖ ـيـنــج ⁾ ↺", url="https://t.me/TR_E2S_ON_MY_MOoN")], [InlineKeyboardButton(text="اضف البوت الي مجموعتك او قناتك ⚜️", url=f"https://t.me/{bot_username}?startgroup=True")]]
    await message.reply_photo(photo=photo, caption=f"**Started Stream Random **\n\n**𝘚𝘰𝘯𝘨 𝘕𝘢𝘮𝘦 : {title}**\n**Duration Time : {duration}**\n**𝘙𝘦𝘲𝘶𝘦𝘴𝘵𝘴 𝘉𝘺 : {req}**", reply_markup=InlineKeyboardMarkup(button))
    await logs(bot_username, client, message)
   except Exception as es:
    await message.reply_text(f"**{es}**")


@Client.on_message(filters.command(["ذيعصوتي"], ""))
async def broadcastahhudio(_, client: Client, message):
   bot_username = client.me.username
   dev = await get_dev(bot_username)
   if message.chat.id == dev or message.chat.username == "TR_E2S_ON_MY_MOoN":
    x = message.reply_to_message
    if not x:
      return await message.reply_text("قم بالرد علي ملف صوتي لعمل اذاعه صوتيه")
    file_path = await x.download()
    status = None
    m = await message.reply_text("جاري الاذاعه الصوتيه")
    served_chats = []
    text = ""
    chats = await get_served_chats()
    for chat in chats:
        served_chats.append(int(chat["chat_id"]))
    count = 0
    co = 0
    msg = ""
    for served_chat in served_chats:
        try:
            chat_id = served_chat
            original_chat_id = served_chat
            await stop_stream(chat_id)
            await join_call(chat_id, original_chat_id, file_path, video=status)
            count += 1
            await message.reply_text(count)
        except FloodWait as e:
            flood_time = int(e.x)
            if flood_time > 200:
               continue
            await asyncio.sleep(flood_time)
        except Exception as e:
          print(e)
    await message.reply_text(f" تم الاذاعه الي {count} محادثه صوتيه")

@Client.on_message(filters.command(["/play", "play", "/vplay", "شغل", "تشغيل", "فيد", "فيديو"], ""))
async def play(client: Client, message):
  AVATAR = message
  bot_username = client.me.username
  chat_id = message.chat.id
  user_id = message.from_user.id if message.from_user else "TR_E2S_ON_MY_MOoN"
  message_id = message.id 
  button = [[InlineKeyboardButton(text="END", callback_data=f"stop"), InlineKeyboardButton(text="RESUME", callback_data=f"resume"), InlineKeyboardButton(text="PAUSE", callback_data=f"pause")], [InlineKeyboardButton(text="᥉᥆υᖇᥴᥱ✘", url="https://t.me/sourceav"), InlineKeyboardButton(text="GᖇOᑌᑭ✘", url="https://t.me/va_source")], [InlineKeyboardButton(text="₍ 𝑘 𝑖 𝑛 𝑔 || كـ ٖ ـيـنــج ⁾ ↺", url="https://t.me/TR_E2S_ON_MY_MOoN")], [InlineKeyboardButton(text="اضف البوت الي مجموعتك او قناتك ⚜️", url=f"https://t.me/{bot_username}?startgroup=True")]]
  if message.chat.type == ChatType.PRIVATE:
       return await message.reply_text("**لا يمكنك التشغيل هنا للأسف **\n** قم بإضافة البوت اللي مجموعتك للتشغيل**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"اضف البوت لمجموعتك ⚜️", url=f"https://t.me/{bot_username}?startgroup=True")]]))
  if message.sender_chat:
     if not message.chat.type == ChatType.CHANNEL:
      return await message.reply_text("**يمكنك التشغيل ب الحساب الشخصي فقط .⚜️**")
  if not message.reply_to_message:
     if len(message.command) == 1:
       name = await client.ask(message.chat.id, text="**ارسل اللي تريد تشغله ✘**", reply_to_message_id=message.id, filters=filters.user(message.from_user.id), timeout=7)
       rep = await name.reply_text("**جاري التشغيل انتظر قليلاً ..⚜️**")
       name = name.text
     else:
       name = message.text.split(None, 1)[1]
       rep = await message.reply_text("**جاري التشغيل انتظر قليلاً ..⚜️**")
     try:
      results = VideosSearch(name, limit=1)
     except Exception:
      return await message.reply_text("**لم يتم العثور علي نتائج .⚜️**")
     for result in (await results.next())["result"]:
         title = result["title"]
         duration = result["duration"]
         videoid = result["id"]
         yturl = result["link"]
         thumbnail = result["thumbnails"][0]["url"].split("?")[0]
     if "v" in message.command[0] or "ف" in message.command[0]:
       vid = True
     else:
       vid = None
     await rep.edit("**جاري التشغيل انتظر قليلاً ..🔥**")
     results = YoutubeSearch(name, max_results=5).to_dict()
     link = f"https://youtube.com{results[0]['url_suffix']}"
     if await is_served_call(client, message.chat.id):
         chat_id = message.chat.id
         title = title.title()
         file_path = None
         await add(message.chat.id, bot_username, file_path, link, title, duration, videoid, vid, user_id)
         chat = f"{bot_username}{chat_id}"
         position = len(db.get(chat)) - 1
         chatname = f"[{message.chat.title}](https://t.me/{message.chat.username})" if message.chat.username else f"{message.chat.title}"
         chatname = f"{message.author_signature}" if message.author_signature else chatname
         requester = chatname if AVATAR.views else f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
         if message.from_user:
          if message.from_user.photo:
           photo_id = message.from_user.photo.big_file_id
           photo = await client.download_media(photo_id)
         elif message.chat.photo:
          photo_id = message.chat.photo.big_file_id
          photo = await client.download_media(photo_id)
         else:
          AVATAR = await client.get_chat("TR_E2S_ON_MY_MOoN")
          AVATARphoto = AVATAR.photo.big_file_id
          photo = await client.download_media(AVATARphoto)
         photo = await gen_thumb(videoid, photo)
         await message.reply_photo(photo=photo, caption=f"**Add Track To Playlist » {position}**\n\n**𝘚𝘰𝘯𝘨 𝘕𝘢𝘮𝘦 : {title[:18]}**\n**Duration Time : {duration}**\n**𝘙𝘦𝘲𝘶𝘦𝘴𝘵𝘴 𝘉𝘺 : {requester}**", reply_markup=InlineKeyboardMarkup(button))
         await logs(bot_username, client, message)
     else:
         chat_id = message.chat.id
         title = title.title()
         file_path = None
         await add_active_chat(chat_id)
         await add_served_call(client, chat_id)
         if vid:
           await add_active_video_chat(chat_id)
         await add(message.chat.id, bot_username, file_path, link, title, duration, videoid, vid, user_id)
         c = await join_call(client, message_id, chat_id, bot_username, file_path, link, vid)
         if not c:
            await remove_active(bot_username, chat_id)
            return await rep.delete()
         chatname = f"[{message.chat.title}](https://t.me/{message.chat.username})" if message.chat.username else f"{message.chat.title}"
         chatname = f"{message.author_signature}" if message.author_signature else chatname
         requester = chatname if AVATAR.views else f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
         if message.from_user:
          if message.from_user.photo:
           photo_id = message.from_user.photo.big_file_id
           photo = await client.download_media(photo_id)
         elif message.chat.photo:
          photo_id = message.chat.photo.big_file_id
          photo = await client.download_media(photo_id)
         else:
          AVATAR = await client.get_chat("TR_E2S_ON_MY_MOoN")
          AVATARphoto = AVATAR.photo.big_file_id
          photo = await client.download_media(AVATARphoto)
         photo = await gen_thumb(videoid, photo)
         await message.reply_photo(photo=photo, caption=f"**𝘗𝘭𝘢𝘺𝘪𝘯𝘨 𝘕𝘰𝘸**\n\n**𝘚𝘰𝘯𝘨 𝘕𝘢𝘮𝘦 : {title[:18]}**\n**Duration Time : {duration}**\n**𝘙𝘦𝘲𝘶𝘦𝘴𝘵𝘴 𝘉𝘺 : {requester}**", reply_markup=InlineKeyboardMarkup(button))
         await logs(bot_username, client, message)
     try:
      os.remove(photo)
     except:
      pass
     await rep.delete()
  else:
       rep = await message.reply_text("**جاري تشغيل الملف الصوتي .🔥**")
       if not message.reply_to_message.media:
         return 
       photo = "https://graph.org/file/9cdbc1531679dc7a507f8.jpg"
       if message.reply_to_message.video or message.reply_to_message.document:
           vid = True
       else:
           vid = None
       file_path = await message.reply_to_message.download()
       if message.reply_to_message.audio:
         file_name = message.reply_to_message.audio
       elif message.reply_to_message.voice:
         file_name = message.reply_to_message.voice
       elif message.reply_to_message.video:
         file_name = message.reply_to_message.video
       else:
         file_name = message.reply_to_message.document
       title = file_name.file_name
       duration = seconds_to_min(file_name.duration)
       link = None
       if await is_served_call(client, message.chat.id):
         chat_id = message.chat.id
         videoid = None
         await add(message.chat.id, bot_username, file_path, link, title, duration, videoid, vid, user_id)
         chat = f"{bot_username}{chat_id}"
         position = len(db.get(chat)) - 1
         chatname = f"[{message.chat.title}](https://t.me/{message.chat.username})" if message.chat.username else f"{message.chat.title}"
         chatname = f"{message.author_signature}" if message.author_signature else chatname
         requester = chatname if AVATAR.views else f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
         await message.reply_photo(photo=photo, caption=f"**Add Track To Playlist » {position}**\n\n**𝘚𝘰𝘯𝘨 𝘕𝘢𝘮𝘦 : {title}**\n**Duration Time {duration}**\n**𝘙𝘦𝘲𝘶𝘦𝘴𝘵𝘴 𝘉𝘺 : {requester}**", reply_markup=InlineKeyboardMarkup(button))
         await logs(bot_username, client, message)
       else:
         chat_id = message.chat.id
         videoid = None
         await add_active_chat(chat_id)
         await add_served_call(client, chat_id)
         if vid:
            await add_active_video_chat(chat_id)
         await add(message.chat.id, bot_username, file_path, link, title, duration, videoid, vid, user_id)
         c = await join_call(client, message_id, chat_id, bot_username, file_path, link, vid)
         if not c:
            await remove_active(bot_username, chat_id)
            return await rep.delete()
         chatname = f"[{message.chat.title}](https://t.me/{message.chat.username})" if message.chat.username else f"{message.chat.title}"
         chatname = f"{message.author_signature}" if message.author_signature else chatname
         requester = chatname if AVATAR.views else f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
         await message.reply_photo(photo=photo, caption=f"**𝘗𝘭𝘢𝘺𝘪𝘯𝘨 𝘕𝘰𝘸**\n\n**𝘚𝘰𝘯𝘨 𝘕𝘢𝘮𝘦 : {title}**\n**Duration Time {duration}**\n**𝘙𝘦𝘲𝘶𝘦𝘴𝘵𝘴 𝘉𝘺 : {requester}**", reply_markup=InlineKeyboardMarkup(button))
         await logs(bot_username, client, message)
  try:
      os.remove(photo)
  except:
      pass
  await rep.delete()

@Client.on_message(filters.command("تخ", ""))
async def tiii(client, message):
   bot_username = client.me.username
   user = await get_userbot(bot_username)
   raw_list = []
   async for msg in user.get_chat_history(""):
       print(msg)
       if msg.text:
         text = msg.text
         raw_list.append(text)
   x = random.choice(raw_list)
   await message.reply_text(f"**{x}**")
