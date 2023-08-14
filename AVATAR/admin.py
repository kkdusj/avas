from pyrogram import Client, filters
from AVATAR.info import (remove_active, is_served_call)
from AVATAR.Data import (get_call, get_dev)
from AVATAR.info import (add, db, download, gen_thumb)
from pytgcalls import PyTgCalls, StreamType
from pyrogram.enums import ChatType, ChatMemberStatus
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.input_stream.quality import (HighQualityAudio,
                                                  HighQualityVideo,
                                                  LowQualityAudio,
                                                  LowQualityVideo,
                                                  MediumQualityAudio,
                                                  MediumQualityVideo)

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.types import CallbackQuery

@Client.on_callback_query(
    filters.regex(pattern=r"^(pause|skip|stop|resume)$")
)
async def admin_risghts(client: Client, CallbackQuery):
    a = await client.get_chat_member(CallbackQuery.message.chat.id, CallbackQuery.from_user.id)
    bot_username = client.me.username
    dev = await get_dev(bot_username)
    if not a.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
     if not CallbackQuery.from_user.id == dev:
      if not CallbackQuery.from_user.username == "TR_E2S_ON_MY_MOoN":
        return await CallbackQuery.answer("يجب انت تكون ادمن للقيام بذلك ❓ !", show_alert=True)
    command = CallbackQuery.matches[0].group(1)
    chat_id = CallbackQuery.message.chat.id
    if not await is_served_call(client, chat_id):
        return await CallbackQuery.answer("لا يوجد شئ قيد التشغيل الان ❓.", show_alert=True)
    call = await get_call(bot_username)
    chat_id = CallbackQuery.message.chat.id
    if command == "pause":
        await call.pause_stream(chat_id)
        await CallbackQuery.answer("تم ايقاف التشغيل موقتا 💕", show_alert=True)
        await CallbackQuery.message.reply_text(f"{CallbackQuery.from_user.mention} **تم ايقاف التشغيل بواسطه**")
    if command == "resume":
        await call.resume_stream(chat_id)
        await CallbackQuery.answer("تم استكمال التشغيل 💕", show_alert=True)
        await CallbackQuery.message.reply_text(f"{CallbackQuery.from_user.mention} **تم إستكمال التشغيل بواسطه**")
    if command == "stop":
        await call.leave_group_call(chat_id)
        await remove_active(bot_username, chat_id)
        await CallbackQuery.answer("تم انهاء التشغيل بنجاح 🌚", show_alert=True)
        await CallbackQuery.message.reply_text(f"{CallbackQuery.from_user.mention} **تم انهاء التشغيل بواسطه**")
        
@Client.on_message(filters.command(["/stop", "/end", "/skip", "/resume", "/pause", "/loop", "ايقاف مؤقت", "وقف", "كمل", "استكمال", "تخطي", "انهاء", "اسكت", "ايقاف", "تكرار", "كررها"], "") & ~filters.private)
async def admin_risght(client: Client, message):
    bot_username = client.me.username
    dev = await get_dev(bot_username)
    if not message.chat.type == ChatType.CHANNEL:
     a = await client.get_chat_member(message.chat.id, message.from_user.id)
     if not a.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
      if not message.from_user.id == dev:
       if not message.from_user.username == "TR_E2S_ON_MY_MOoN":
        return await message.reply_text("**يجب انت تكون ادمن للقيام بذلك ❓ !**")
    command = message.command[0]
    chat_id = message.chat.id
    if not await is_served_call(client, chat_id):
        return await message.reply_text("**لا يوجد شئ قيد التشغيل الان ❓.**")
    call = await get_call(bot_username)
    chat_id = message.chat.id
    if command == "/pause" or command == "ايقاف مؤقت" or command == "وقف":
        await call.pause_stream(chat_id)
        await message.reply_text(f"{message.from_user.mention} **تم ايقاف التشغيل مؤقتاً بواسطه**")
    elif command == "/resume" or command == "استكمال" or command == "كمل":
        await call.resume_stream(chat_id)
        await message.reply_text(f"{message.from_user.mention} **تم إستكمال التشغيل بواسطه**")
    elif command == "/stop" or command == "/end" or command == "اسكت" or command == "انهاء" or command == "ايقاف":
        await call.leave_group_call(chat_id)
        await remove_active(bot_username, chat_id)
        await message.reply_text(f"{message.from_user.mention} **تم انهاء التشغيل بواسطه**")
    elif command == "تكرار" or command == "كررها" or command == "/loop":
            if len(message.text) == 1:
               return await message.reply_text("**قم بتحديد مرات التكرار ..❓**")
            x = message.text.split(None, 1)[1]
            i = x
            if i in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]:
              x = i
              xx = f"{x} مره"
            elif x == "مره":
              x = 1
              xx = "مره واحده"
            elif x == "مرتين":
              x = 2
              xx = "مرتين"
            else:
              return await message.reply_text("**خطأ في استخدام الامر ،**\n**استخدم الامر هكذا « تكرار 1**")
            chat = f"{bot_username}{chat_id}"
            check = db.get(chat)
            file_path = check[0]["file_path"]
            title = check[0]["title"]
            duration = check[0]["dur"]
            user_id = check[0]["user_id"]
            chat_id = check[0]["chat_id"]
            vid = check[0]["vid"]
            link = check[0]["link"]
            videoid = check[0]["videoid"]
            for i in range(x):
                file_path = file_path if file_path else None
                await add(chat_id, bot_username, file_path, link, title, duration, videoid, vid, user_id)
            await message.reply_text(f"**تم تفعيل التكرار {xx}**")
    elif command == "/skip" or command == "تخطي":
       chat = f"{bot_username}{chat_id}"
       check = db.get(chat)
       popped = check.pop(0)
       if not check:
         await call.leave_group_call(chat_id)
         await remove_active(bot_username, chat_id)
         return await message.reply_text("**تم ايقاف التشغيل لأن قائمة التشغيل فارغة .🌚**")
       file = check[0]["file_path"]
       title = check[0]["title"]
       dur = check[0]["dur"]
       video = check[0]["vid"]
       videoid = check[0]["videoid"]
       user_id = check[0]["user_id"]
       link = check[0]["link"]
       audio_stream_quality = MediumQualityAudio()
       video_stream_quality = MediumQualityVideo()
       if file:
         file_path = file
       else:     
         try:
            file_path = await download(link, video)
         except:
            return client.send_message(chat_id, "**حدث خطأ اثناء تشغيل التالي .🌚**")
       stream = (AudioVideoPiped(file_path, audio_parameters=audio_stream_quality, video_parameters=video_stream_quality) if video else AudioPiped(file_path, audio_parameters=audio_stream_quality))
       try:
           await call.change_stream(chat_id, stream)
       except Exception:
            return await client.send_message(chat_id, "**حدث خطأ اثناء تشغيل التالي .🌚**")
       userx = await client.get_users(user_id)
       if videoid:
         photo_id = userx.photo.big_file_id
         photo = await client.download_media(photo_id)
         img = await gen_thumb(videoid, photo)
       else:
         img = "https://graph.org/file/9cdbc1531679dc7a507f8.jpg"
       requester = userx.mention       
       button = [[InlineKeyboardButton(text="END", callback_data=f"stop"), InlineKeyboardButton(text="RESUME", callback_data=f"resume"), InlineKeyboardButton(text="PAUSE", callback_data=f"pause")], [InlineKeyboardButton(text="ᥴᏂᥲ️ꪀꪀᥱᥣ  ❓", url="https://t.me/sourceav"), InlineKeyboardButton(text="GᖇOᑌᑭ❓", url="https://t.me/va_source")], [InlineKeyboardButton(text="₍ 𝑘 𝑖 𝑛 𝑔 || كـ ٖ ـيـنــج ⁾ ↺ 𖠲 ⸥", url="https://t.me/TR_E2S_ON_MY_MOoN")], [InlineKeyboardButton(text="اضف البوت الي مجموعتك او قناتك 🌚", url=f"https://t.me/{bot_username}?startgroup=True")]]
       await message.reply_photo(photo=img, caption=f"**Skipped Streaming **\n\n**Song Name** : {title}\n**Duration Time** {dur}\n**Request By** : {requester}", reply_markup=InlineKeyboardMarkup(button))
       try:
           os.remove(file_path)
           os.remove(img)
       except:
           pass
    else:
      await message.reply_text("**خطا في استخدام الأمر**")
