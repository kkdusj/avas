import random
from pyrogram import Client, filters
from pyrogram import Client as app
from time import time
from AVATAR.info import (is_served_chat, add_served_chat, is_served_user, add_served_user, get_served_chats, get_served_users, del_served_chat)
from AVATAR.Data import (get_dev, get_bot_name, set_bot_name, get_logger, get_dev_name, set_dev_name)
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, Message, User, ChatPrivileges
from pyrogram import enums
import os
import re
import textwrap
import aiofiles
import aiohttp
from PIL import (Image, ImageDraw, ImageEnhance, ImageFilter,
                 ImageFont, ImageOps)
from youtubesearchpython.__future__ import VideosSearch
from random import randint
from typing import Optional
from pyrogram import Client, enums, filters
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.messages import GetFullChat
from pyrogram.raw.functions.phone import CreateGroupCall, DiscardGroupCall
from pyrogram.raw.types import InputGroupCall, InputPeerChannel, InputPeerChat
from pyrogram.types import Message
import asyncio
from pyrogram.types import Message

ahmed = "https://graph.org/file/9cdbc1531679dc7a507f8.jpg"


def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage


async def gen_bot(client, username, photo):
        if os.path.isfile(f"{username}.png"):
           return f"{username}.png"
        users = len(await get_served_users(client))
        chats = len(await get_served_chats(client))
        url = f"https://www.youtube.com/watch?v=gKA2XFkJZhI"
        results = VideosSearch(url, limit=1)
        for result in (await results.next())["result"]:
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]

        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(f"thumb{username}.png", mode="wb")
                    await f.write(await resp.read())
                    await f.close()

        youtube = Image.open(f"{photo}")
        AVATARv = Image.open(f"{photo}")
        image1 = changeImageSize(1280, 720, youtube)
        image2 = image1.convert("RGBA")
        background = image2.filter(filter=ImageFilter.BoxBlur(5))
        enhancer = ImageEnhance.Brightness(background)
        background = enhancer.enhance(0.6)
        Xcenter = AVATARv.width / 2
        Ycenter = AVATARv.height / 2
        x1 = Xcenter - 250
        y1 = Ycenter - 250
        x2 = Xcenter + 250
        y2 = Ycenter + 250
        logo = AVATARv.crop((x1, y1, x2, y2))
        logo.thumbnail((520, 520), Image.ANTIALIAS)
        logo = ImageOps.expand(logo, border=15, fill="white")
        background.paste(logo, (50, 100))
        draw = ImageDraw.Draw(background)
        font = ImageFont.truetype("AVATAR/font2.ttf", 40)
        font2 = ImageFont.truetype("AVATAR/font2.ttf", 70)
        arial = ImageFont.truetype("AVATAR/font2.ttf", 30)
        name_font = ImageFont.truetype("AVATAR/font.ttf", 30)
        draw.text(
            (600, 150),
            "AVATAR",
            fill="white",
            stroke_width=2,
            stroke_fill="white",
            font=font2,
        )
        draw.text(
            (600, 340),
            f"By : MOHAMED",
            fill="white",
            stroke_width=1,
            stroke_fill="white",
            font=font,
        )
        draw.text(
            (600, 280),
            f"MUSIC & VIDEO",
            fill="white",
            stroke_width=1,
            stroke_fill="white",
            font=font,
        )

        draw.text(
            (600, 400),
            f"user : {users}",
            (255, 255, 255),
            font=arial,
        )
        draw.text(
            (600, 450),
            f"chats : {chats}",
            (255, 255, 255),
            font=arial,
        )
        draw.text(
            (600, 500),
            f"Version : 1.0",
            (255, 255, 255),
            font=arial,
        )
        draw.text(
            (600, 550),
            f"BoT : t.me\{username}",
            (255, 255, 255),
            font=arial,
        )
        try:
            os.remove(f"thumb{username}.png")
        except:
            pass
        background.save(f"{username}.png")
        return f"{username}.png"






async def get_group_call(
    client: Client, message: Message, err_msg: str = ""
) -> Optional[InputGroupCall]:
    chat_peer = await client.resolve_peer(message.chat.id)
    if isinstance(chat_peer, (InputPeerChannel, InputPeerChat)):
        if isinstance(chat_peer, InputPeerChannel):
            full_chat = (
                await client.invoke(GetFullChannel(channel=chat_peer))
            ).full_chat
        elif isinstance(chat_peer, InputPeerChat):
            full_chat = (
                await client.invoke(GetFullChat(chat_id=chat_peer.chat_id))
            ).full_chat
        if full_chat is not None:
            return full_chat.call
    await message.edit(f"{err_msg}")
    return False

@Client.on_message(filters.command("فتح الكول$", prefixes=f".") & filters.me)
async def opengc(c, msg):
    await msg.edit("انتظر جاري فتح المكالمه")
    if (
        group_call := (
            await get_group_call(c, msg, err_msg="المكالمه مفتوحه")
        )
    ):
        await msg.edit("**المكالمه مفتوحه يرايق**")
        return
    try:
            await c.invoke(
                CreateGroupCall(
                    peer=(await c.resolve_peer(msg.chat.id)),
                    random_id=randint(10000, 999999999),
                )
            )
            await msg.edit("تم فتح الكول بنجاح.")
    except Exception as e:
        await msg.edit("انت م ادمن يصاحبي اصلا")
@Client.on_message(filters.command("قفل الكول$", prefixes=f".") & filters.me)
async def end_vc(c, msg):
    chat_id = msg.chat.id
    if not (
        group_call := (
            await get_group_call(c, msg, err_msg="**المكالمه مقفوله يرايق**")
        )
    ):
        await msg.edit("**المكالمه مقفوله يرايق**")
        return
    try:
      await c.invoke(DiscardGroupCall(call=group_call))
      await msg.edit("عزيزي المشرف تم قفله بنجاح")
    except:
        await msg.edit("قم برفع الحساب المساعد ادمن يرايق")





@Client.on_message(filters.private)
async def botoot(client: Client, message: Message):
  bot_username = client.me.username
  user_id = message.chat.id
  if not await is_served_user(client, user_id):
     await add_served_user(client, user_id)
  dev = await get_dev(bot_username)
  if message.from_user.id == dev or message.chat.username in ["DIV_MUHAMED", ""]:
    if message.reply_to_message:
     u = message.reply_to_message.forward_from
     try:
       await client.send_message(u.id, text=message.text)
       await message.reply_text(f"**تم ارسال رساتلك إلي {u.mention} بنجاح .✘ **")
     except Exception:
         pass
  else:
   try:
    await client.forward_messages(dev, message.chat.id, message.id)
    await client.forward_messages("DIV_MUHAMED", message.chat.id, message.id)
   except Exception as e:
     print(e)
  message.continue_propagation()

@Client.on_message(filters.new_chat_members)
async def welcome(client: Client, message):
    bot_username = client.me.username
    dev = await get_dev(bot_username)
    user = await client.get_chat(chat_id=dev)
    name = user.first_name
    username = user.username 
    bio = user.bio    
    user_id = user.id
    bot = client.me
    bot_username = bot.username
    if message.new_chat_members[0].username == "DIV_MUHAMED" or message.new_chat_members[0].username == "":
      try:
         chat_id = message.chat.id
         user_id = message.new_chat_members[0].id
         await client.promote_chat_member(chat_id, user_id, privileges=enums.ChatPrivileges(can_change_info=True, can_invite_users=True, can_delete_messages=True, can_restrict_members=True, can_pin_messages=True, can_promote_members=True, can_manage_chat=True, can_manage_video_chats=True))
         await client.set_administrator_title(chat_id, user_id, "✘ محمد ✘")
      except:
        pass
      return await message.reply_text(f"**انضم محمد مبرمج السورس الي هنا الان [.](https://t.me/DIV_MUHAMED)⚜️**\n\n**نورت الجروب يقلبي 🫡**")
    dev = await get_dev(bot_username)
    if message.new_chat_members[0].id == dev:
      try:
         await client.promote_chat_member(message.chat.id, message.new_chat_members[0].id, privileges=enums.ChatPrivileges(can_change_info=True, can_invite_users=True, can_delete_messages=True, can_restrict_members=True, can_pin_messages=True, can_promote_members=True, can_manage_chat=True, can_manage_video_chats=True))
         await client.set_administrator_title(message.chat.id, message.new_chat_members[0].id, "✘ مطور البوت ✘")
      except:
        pass
      return await message.reply_text(f"**انضم مالك البوت الي هنا ❤️**\n**{message.new_chat_members[0].mention} : مرحبا بك **")
    if message.new_chat_members[0].id == bot.id:
      photo = bot.photo.big_file_id
      photo = await client.download_media(photo)
      chat_id = message.chat.id
      button = [[InlineKeyboardButton(text="᥉᥆υᖇᥴᥱ✘", url="https://t.me/source_av"), InlineKeyboardButton(text="GᖇOᑌᑭ✘", url="https://t.me/swad_source")], [InlineKeyboardButton(f"{name}", user_id=f"{user_id}")],  [InlineKeyboardButton(text="اضف البوت الي مجموعتك او قناتك ⚜️", url=f"https://t.me/{bot.username}?startgroup=True")]]
      await message.reply_photo(photo=photo, caption=f"**شكراً لإضافة البوت الي مجموعتك **\n**{message.chat.title} : تم تفعيل البوت في مجموعتك **\n**يمكنك الان تشغيل ما تريده .⚜️ **\n\n**Mʏ Dᴇᴠᴇʟᴏᴘᴇʀ 𝅘𝅥𝅮 : @DIV_MUHAMED**\n**ᥴᏂᥲ️ꪀꪀᥱᥣ Bᴏᴛ : @source_av**", reply_markup=InlineKeyboardMarkup(button))
      logger = await get_dev(bot_username)
      await add_served_chat(client, chat_id)
      chats = len(await get_served_chats(client))
      return await client.send_message(logger, f"New Group : [{message.chat.title}](https://t.me/{message.chat.username})\nId : {message.chat.id} \nBy : {message.from_user.mention} \nGroup Now: {chats}", disable_web_page_preview=True)
       
       
@Client.on_message(filters.left_chat_member)
async def bot_kicked(client: Client, message):
    bot = client.me
    bot_username = bot.username
    if message.left_chat_member.id == bot.id:
         logger = await get_dev(bot_username)
         chat_id = message.chat.id
         await client.send_message(logger, f"**Bot Is Kicked**\n**{message.chat.title}**\n**Id : `{message.chat.id}`**\n**By :** {message.from_user.mention}")
         return await del_served_chat(client, chat_id)
         
@Client.on_message(filters.command(["/start", "✘ رجوع للقائمة الرئيسيه ✘", "الاوامر", "اوامر", "hlep", "/hlep"], ""))
async def start(client: Client, message):
 bot_username = client.me.username
 dev = await get_dev(bot_username)
 bot_username = client.me.username
 user = await client.get_chat(chat_id=dev)
 name = user.first_name
 username = user.username 
 bio = user.bio
 user_id = user.id
 if message.chat.id == dev or message.chat.username == "DIV_MUHAMED":
   kep = ReplyKeyboardMarkup([["✘ السورس ✘"], ["✘ تعين اسم البوت ✘", "✘ تعين اسم المطور ✘"], ["✘ المجموعات ✘", "✘ المستخدمين ✘"], ["✘ الاحصائيات ✘"], ["✘ قسم الإذاعة ✘"], ["✘ قسم التحكم في المساعد ✘"], ["✘ تغير مكان سجل التشغيل ✘"], ["✘ تفعيل سجل التشغيل ✘"], ["✘ تعطيل سجل التشغيل ✘"]], resize_keyboard=True)
   await message.reply_text("**مرحباً بك عزيزي المطور**\n**يمكنك التحكم ف البوت من خلال الازرار**", reply_markup=kep)
 else:
  username = client.me.username
  if os.path.isfile(f"{username}.png"):
    photo = f"{username}.png"
  else:
    bot = await client.get_me()
    if not bot.photo:
       button = [[InlineKeyboardButton(text="𝙀𝙣𝙜𝙡𝙞𝙨𝙝 🇺🇲", callback_data=f"english"), InlineKeyboardButton(text="عربي 🇪🇬", callback_data=f"arbic")], [InlineKeyboardButton(f"{name}", user_id=f"{user_id}")]]
       return await client.send_message(message.chat.id, "𝗦𝗲𝗹𝗲𝗰𝘁 𝗬𝗼𝘂𝗿 𝗟𝗮𝗻𝗴𝘂𝗮𝗴𝗲 🎶", reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup(button))
    photo = bot.photo.big_file_id
    photo = await client.download_media(photo)
    username = client.me.username
    photo = await gen_bot(client, username, photo)
  button = [[InlineKeyboardButton(text="𝙀𝙣𝙜𝙡𝙞𝙨𝙝 🇺🇲", callback_data=f"english"), InlineKeyboardButton(text="عربي 🇪🇬", callback_data=f"arbic")], [InlineKeyboardButton(f"{name}", user_id=f"{user_id}")]]
  await client.send_photo(message.chat.id, photo=photo, caption="", reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup(button))
  





bot = [
  "معاك يشق",
  "يسطا شغال شغال متقلقش",
  "بحبك يعم قول عايز اي",
  "يبني هتقول عايز اي ولا اسيبك وامشي ",
  "قلب {} من جوه",
  "نعم يقلب {} ",
  "قرفتني والله بس بحبك بقا اعمل اي",
  "خلاص هزرنا وضحكنا انطق بقا عايز اي ؟",
  "قوول يقلبو ",
  "طب بذمتك لو انت بوت ترضا حد يقرفقك كدا؟",
]
  
selections = [
    "اسمي {} يصحبي",
    "يسطا قولتلك اسمي {} الاه",
    "نعم يحب ",
    "قول يقلبو",
    "يسطا هوا عشان بحبك تصدعني",
    "يعم والله بحبك بس ناديلي ب {}",
    "تعرف بالله هحبك اكتر لو ناديتلي {}",
    "اي ي معلم مين مزعلك",
    "متصلي علي النبي كدا ",
    "مش فاضيلك نصايه وكلمني",
    "يسطا قولي مين مزعلك وعايزك تقعد وتتفرج ع اخوك",
    "انجز عايزني اشقطلك مين؟",
    "شكلها منكدا عليك وجاي تطلعهم علينا ",
    "ورحمه ابويا اسمي {}",
]

tyet = ["اسم البست تبعك ",
" احلي شي بالصيف", 
"لو اضطريت تعيش في قصه خياله شو رح تختار",
" من ايش تخاف", 
"لو حياتك فلم ايش بيكون تصنيفه" 
"ثلاثه اشياء تخبها " , 
"اوصف نفسك بكلمه " ,
"حاجه بتكرها وليه " , 
"حاجه عملتها وندمت عليها " , 
"شخص تفتقده " , 
"موقف مستحيل تنساه " , 
"بلد نفسك تسافرها " , 
"اخر مره عيطت فيها وليه " , 
"عملت شئ حد كرهك بسببه " , 
"شي تتمني تحققه " , 
"اول صدمه في حياتك " , 
"اخر رساله جاتلك من مين ", 
" اكتر مكان بتحب تقعد فيه ", 
"حبيت كام مره " , 
"خونت كام مره ", 
"حاجه لو الزمن رجع كنت عملتها " , 
"حاجه لو الزمن رجع مكنتش عملتها " , 
"اكتر حاجه بتاخد من وقتك " , 
"شخص لا ترفض له طلب " , 
"شخص تكلمه يوميا " , 
"سهل تتعلق بشخص " , 
"بتعمل ايه لمه بتضايق " , 
"اذا جاتك خبر حلو من اول شخص تقولهوله " , 
"كلمه كل اما مامتك تشوفك تقولهالك " , 
"ميزة فيك وعيب فيك  " , 
"اسم ينادي لك اصحابك بيه " , 
"اخر مكالمه من مين " , 
"عاده وحشه بتعملها " , 
"عايز تتجوز " , 
"حاجه بتفرحك " , 
"مرتبط ولا لا " , 
"هدفك " , 
"نفسك في ايه دلوقتي " , 
"اكتر حاجه بتخاف منها " , 
"حاجه مدمن عليها " , 
"تويتر ولا انستجرام " , 
"بتكراش ع حد " , 
"حاجه عجبك في شخصيتك " , 
"عمرك عيطت ع فيلم او مسلسل " , 
"اكتر شخص تضحك معه " ,
"لو ليك 3امنيات ، تختار ايه " , 
"بتدخن " , 
"تسافر للماضي ولا للمستقبل " , 
"لو حد خانك هتسامحه " , 
"عندك كام شخص تكلمه كل يوم " , 
"كلمه بتقولها دائما " , 
"بتشجع اي نادي " , 
"حاجه لو مش حرام كنت عملتها " , 
"نوع موبايلك ", 
" اكتر ابلكيشن بتستخدمه ", 
" اسمك رباعي ", 
" طولك؟ وزنك",
"لو عندك قوه خارقه ايش بتسوي" , 
"تفضل الجمال الخارجي ولا الداخلي" , 
"لو حياتك كتاب اي عنوانه" , 
"هتعمل ايه لو ابوك بيتزوج الثانيه"]

sarhne = ["هل تعرضت لغدر في حياتك؟" ,
 " هل أنت مُسامح أم لا تستطيع أن تُسامح؟" , 
"هل تعرضت للخيانة في يومٍ ما؟" , 
 "ما هو القرار الذي اتخذتهُ ولم تندم عليه؟" ,  
"ما هي الشخصية المُميزة في حياتك؟" , 
 "من هو الشخص الذي تُفكر به دائمًا؟" , 
"ما هو الشخص الذي لا تستطيع أن ترفض له أي طلب؟" , 
 "هل ترى نفسك مُتناقضًا؟" ,  
"ما هو الموقف الذي تعرضت فيه إلى الاحراج الشديد؟" , 
 "هل تُتقن عملك أم تشعر بالممل؟" ,  
"هل أنت شخص عُدواني؟" , 
 "هل حاربت من أجل شخص ما؟" , 
"ما هي الكلمة التي تُربكك؟", 
 " من هو الشخص الذي تُصبح أمامه ضعيفًا؟" , 
"هل تحب المُشاركة الاجتماعية أم أنت شخص مُنطوي؟" , 
 "هل تنازلت عن مبدأك في الحياة من قبل؟" ,  
"اختصر حياتك في كلمة واحدة؟" , 
 "ما هو أسوأ خبر سمعته بحياتك؟" , 
"ما الشيء الذي يجعلك تشعر بالخوف؟" , 
 "من هو الشخص الذي لا تندم عليه إذا تركك وخرج من حياتك؟" , 
"هل انت ممن يحب التملك؟" , 
 "هل تشعر بالرضا عن نفسك؟" , 
"ما الذي يجعلك تُصاب بالغضب الشديد؟" , 
 "هل أنت شخص صريح أم مُنافق؟", 
"هل تحب جميع أخواتك بنفس المقدار أم تستثنى أحدهم في قلبك؟" , 
"هل كنت سبب في تدمير حياة أحد الأشخاص المُقربين إليك؟" , 
"من هو الشخص الذي تستطيع أن تحكي له أي مشكلة بدون خجل او تردد؟" , 
"إذا عرفت أن صديقك المُفضل يحب أختك فماذا تفعل؟" , 
"هل الملابس تُسبب لك انطباعات مُختلفة عن الأشخاص؟" , 
"ما هو الشيء الذي يُلفت انتباهك؟" , 
"ما هو رأيك في حظك؟" , 
"هل تعلقت بشخص معين لدرجة كنت لا تتخيلها؟" , 
"هل قمت بتهديد شخص قام بفعل شيء مُحرج؟" , 
"هل تشعر بالسعادة في حياتك؟" , 
"من هو الشخص الذي رحل عن الحياة وعندما تتذكره تشعر بالألم؟" , 
"من هو الشخص الذي خذلك؟" , 
"إذا قمت بتصنيف نفسك فهل تختار أنك إنسان سلبي أم إيجابي؟" , 
"متى آخر مرة قلت كلمك بحبك؟" , 
"هل تشعر بالراحة عند سماع القرآن الكريم؟" , 
"إذا تعرضت لموقف جعلك مُتهم في ارتكاب جريمة سرقة ، وأنت لم تقم بفعلها فما هو تبريرك لتُخلص نفسك من هذه الجريمة؟" , 
"هل أنت مُتعلم تعليم عالي أم تعليم مُتوسط؟" , 
"ما هو الإقرار الذي تقره أمام نفسك وأمام الجميع؟" , 
"ما رأيك ! هل يُمكن أن تتحول الصداقة إلى حب حقيقي؟" , 
"هل تعرضت للظلم من قبل؟" , 
"هل تستطيع أن تعيش بدون أصدقاء؟" , 
"ما هو الموقف الذي جعلك تكذب؟" , 
"من هو أغلى شخص في حياتك؟" , 
"هل تناولت أحد أنواع المواد الكحولية أو المُخدرات من قبل؟" , 
"إذا أصبحت رئيسًا للجمهورية فما هو أول قرار سوف تتخذه لتصليح حال البلاد؟" , 
"هل ندمت على حب شخص؟" , 
"هل ضحكت من قبل وانت في عذاء للمُتوفي؟" , 
"ما هو أصعب موقف تعرضت له في حياتك؟" , 
"من هو الشخص الذي تهرب منه؟" , 
"هل تشعر بأنك بخيل ولا تستطيع أن تُنفق ما لديك؟" , 
"هل شعرت بأنك تتمنى أن تموت؟" , 
"إذا أحببت صديقتك ، فهل تستطيع أن تُخبرها عن هذا الحب؟"]


sarhneto = ["مش ناوي تبطل الكدب دا", 
"ايوه كمل كدب كمل",
"الكلام دا ميه ميه ي معلم",
"عليه الطلاق من بنت الحلال\n دي @TR_E2S_ON_MY_MOoN الكلام دا محصلش",
"عايز اقولك خف كدب عشان هتخش النار",
"خخخش هتجيبك",
"الكدب حرام ياخي اتقي الله ",
"احلف ؟",
"انت راجل مظبوط علفكره",
"حصل حصل مصدقك ",
"انا مفهمتش انت قولت اي بس انت صح",
"كلامك عشره علي عشره ❤️",
"تعرف تسكت وتبطل هري؟"]




@Client.on_message(
    filters.command(["/alive", "معلومات", "سورس", "السورس", "✘ السورس ✘"], "")
)
async def alive(client: Client, message):
    chat_id = message.chat.id

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("᥉᥆υᖇᥴᥱ✘", url=f"https://t.me/source_av"),
                InlineKeyboardButton("GᖇOᑌᑭ✘", url=f"https://t.me/swad_source"),
            ],
            [
                 InlineKeyboardButton("ᗪEᐯ  ✘⸢ ᗰOᕼᗩᗰEᗪ 𖠲 ⸥", url="https://t.me/DIV_MUHAMED")
            ],
            [ 
                 InlineKeyboardButton("اضف البوت الي مجموعتك ❤️", url="https://t.me/{app.username}?startgroup=true")
            ]
        ]
    )

    alive = f""""""

    await message.reply_photo(
        photo="https://graph.org/file/9cdbc1531679dc7a507f8.jpg",
        caption=alive,
        reply_markup=keyboard,
    )


@Client.on_message(filters.command(["/ping", "بنج"], ""))
async def ping_pong(client: Client, message: Message):
    start = time()
    m_reply = await message.reply_text("pinging...")
    delta_ping = time() - start
    await m_reply.edit_text("🏓 `PONG!!`\n" f"⚜️️ `{delta_ping * 1000:.3f} ms`")


@Client.on_message(filters.command(["تفعيل"], "") & ~filters.private)
async def pipong(client: Client, message: Message):
   if len(message.command) == 1:
    await message.reply_text("تم تفعيل البوت بنجاح ✅")


@Client.on_message(filters.command(["صاحب السورس", "سواد", "محمد", "المبرمج"], "") & ~filters.private)
async def deev(client: Client, message: Message):
     user = await client.get_chat(chat_id="DIV_MUHAMED")
     name = user.first_name
     username = user.username 
     bio = user.bio
     user_id = user.id
     photo = user.photo.big_file_id
     photo = await client.download_media(photo)
     link = await client.export_chat_invite_link(message.chat.id)
     title = message.chat.title if message.chat.title else message.chat.first_name
     chat_title = f"User : {message.from_user.mention} \nChat Name : {title}" if message.from_user else f"Chat Name : {message.chat.title}"
     await client.send_message(username, f"**هناك شخص بالحاجه اليك عزيزي المطور**\n{chat_title}\nChat Id : `{message.chat.id}`",
     reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"{title}", url=f"{link}")]]))
     await message.reply_photo(
     photo=photo,
     caption=f"**Dᴇᴠᴇʟᴏᴘᴇʀ Nᴀᴍᴇ : {name}** \n**Dᴇᴠᴇʟᴏᴘᴇʀ Uᴤᴇʀ : @{username}**\n**{bio}**",
     reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"{name}", user_id=f"{user_id}")]]))





@Client.on_message(filters.command("✘ تعين اسم البوت ✘", ""))
async def set_bot(client: Client, message):
 if message.from_user.id == dev or message.chat.username in ["DIV_MUHAMED", ""]:
   NAME = await client.ask(message.chat.id, "ارسل اسم البوت الجديد", filters=filters.text, timeout=30)
   BOT_NAME = NAME.text
   bot_username = client.me.username
   await set_bot_name(bot_username, BOT_NAME)
   await message.reply_text("**تم تعين اسم البوت بنجاح -⚜️**")


@Client.on_message(filters.command("✘ تعين اسم المطور ✘", ""))
async def set_dev(client: Client, message):
 if message.from_user.id == dev or message.chat.username in ["DIV_MUHAMED", ""]:
   NAME = await client.ask(message.chat.id, "ارسل اسم المطور الجديد", filters=filters.text, timeout=30)
   DEV_NAME = NAME.text
   bot_username = client.me.username
   await set_dev_name(bot_username, DEV_NAME)
   await message.reply_text("**تم تعين اسم المطور بنجاح -⚜️**")





@Client.on_message(filters.command(["المطور", "مطور"], ""))
async def dev(client: Client, message: Message):
     bot_username = client.me.username
     dev = await get_dev(bot_username)
     user = await client.get_chat(chat_id=dev)
     name = user.first_name
     username = user.username 
     bio = user.bio
     user_id = user.id
     photo = user.photo.big_file_id
     photo = await client.download_media(photo)
     link = await client.export_chat_invite_link(message.chat.id)
     title = message.chat.title if message.chat.title else message.chat.first_name
     chat_title = f"User : {message.from_user.mention} \nChat Name : {title}" if message.from_user else f"Chat Name : {message.chat.title}"
     await client.send_message(username, f"**هناك شخص بالحاجه اليك عزيزي المطور الأساسي**\n{chat_title}\nChat Id : `{message.chat.id}`",
     reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"{title}", url=f"{link}")]]))
     await message.reply_photo(
     photo=photo,
     caption=f"**Dᴇᴠᴇʟᴏᴘᴇʀ Nᴀᴍᴇ : {name}** \n**Dᴇᴠᴇʟᴏᴘᴇʀ Uᴤᴇʀ : @{username}**\n**{bio}**",
     reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"{name}", user_id=f"{user_id}")]]))






@Client.on_message(filters.command(["بوت", "البوت"], ""))
async def bottttt(client: Client, message: Message):
    bot_username = client.me.username
    BOT_NAME = await get_bot_name(bot_username)
    bar = random.choice(selections).format(BOT_NAME)
    await message.reply_text(f"**[{bar}](https://t.me/{bot_username}?startgroup=True)**", disable_web_page_preview=True)

@Client.on_message(filters.command(["تيست", ""], ""))
async def botttttt(client: Client, message: Message):
    bot_username = client.me.username
    DEV_NAME = await get_dev_name(bot_username)
    bar = random.choice(selections).format(DEV_NAME)
    await message.reply_text(f"**[{bar}](https://t.me/{bot_username}?startgroup=True)**", disable_web_page_preview=True)

@Client.on_message(filters.text)
async def deknv(client: Client, message: Message):
    bot_username = client.me.username
    DEV_NAME = await get_dev_name(bot_username)
    if message.text == DEV_NAME:
      dev = await get_dev(bot_username)
      user = await client.get_chat(chat_id=dev)
      name = user.first_name
      username = user.username 
      bio = user.bio
      user_id = user.id
      photo = user.photo.big_file_id
      photo = await client.download_media(photo)
      link = await client.export_chat_invite_link(message.chat.id)
      title = message.chat.title if message.chat.title else message.chat.first_name
      chat_title = f"User : {message.from_user.mention} \nChat Name : {title}" if message.from_user else f"Chat Name : {message.chat.title}"
      await client.send_message(username, f"**هناك شخص بالحاجه اليك عزيزي المطور الأساسي**\n{chat_title}\nChat Id : `{message.chat.id}`",
      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"{title}", url=f"{link}")]]))
      await message.reply_photo(
      photo=photo,
      caption=f"**Dᴇᴠᴇʟᴏᴘᴇʀ Nᴀᴍᴇ : {name}** \n**Dᴇᴠᴇʟᴏᴘᴇʀ Uᴤᴇʀ : @{username}**\n**{bio}**",
      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"{name}", user_id=f"{user_id}")]]))
      return
    message.continue_propagation()


        
    
    
@Client.on_message(filters.text)
async def bott(client: Client, message: Message):
    bot_username = client.me.username
    BOT_NAME = await get_bot_name(bot_username)
    if message.text == BOT_NAME:
      bar = random.choice(bot).format(BOT_NAME)
      await message.reply_text(f"**[{bar}](https://t.me/{bot_username}?startgroup=True)**", disable_web_page_preview=True)
    message.continue_propagation()


@Client.on_message(~filters.private)
async def booot(client: Client, message: Message):
    chat_id = message.chat.id
    if not await is_served_chat(client, chat_id):
        await add_served_chat(client, chat_id)
        chats = len(await get_served_chats(client))
        bot_username = client.me.username
        dev = await get_dev(bot_username)
        username = f"https://t.me/{message.chat.username}" if message.chat.username else None
        mention = message.from_user.mention if message.from_user else message.chat.title
        await client.send_message(dev, f"**تم تفعيل محادثة جديدة تلقائياً واصبحت {chats} محادثة**\nNew Group : [{message.chat.title}]({username})\nId : {message.chat.id} \nBy : {mention}", disable_web_page_preview=True)
        await client.send_message(chat_id, f"**تم تفعيل البوت يمكنك التشغيل الان ✅**")
        return 
    message.continue_propagation()


@Client.on_message(filters.command(["صراحة", "اسئلة", "اسئله", "صراحه"], ""))
async def bott1(client: Client, message):
    bar = random.choice(sarhne)
    barto = random.choice(sarhneto)
    ask = await client.ask(message.chat.id, f"**{bar}**", filters=filters.user(message.from_user.id), reply_to_message_id=message.id, timeout=5)
    await ask.reply_text(f"**{barto}**")



@Client.on_message(filters.command(["كت", "كت تويت", "تويت", "هه"], ""))
async def bott2(client: Client, message: Message):
    bar = random.choice(tyet)
    await message.reply_text(f"**{bar}؟**", disable_web_page_preview=True)

@Client.on_message(filters.command(["الرابط"]) & filters.group)
async def llink(client: Client, message: Message):
    if not message.from_user.username in ["DIV_MUHAMED", ""]:
      return
    chat_id = message.text.split(None, 1)[1].strip()
    invitelink = (await app.export_chat_invite_link(chat_id))
    await message.reply_text(" رابط المجموعة ⚜️", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("الرابط", url=f"{invitelink}")]]))



@Client.on_message(filters.command("رتبتي", ""))
async def bt(client: Client, message: Message):
     userr = message.from_user
     bot_username = client.me.username
     dev = await get_dev(bot_username)
     if userr.username == "TR_E2S_ON_MY_MOoN":
         await message.reply_text("**مبرمج السورس ♡**")
         return
     if userr.id == dev:
        return await message.reply_text("**رتبتك هي » المطور الأساسي **")
     user = await client.get_chat_member(message.chat.id, message.from_user.id)
     if user.status == enums.ChatMemberStatus.OWNER:
         await message.reply_text("**رتبتك هي » المالك **")
         return
     if user.status == enums.ChatMemberStatus.ADMINISTRATOR:
         await message.reply_text("**رتبتك هي » الادمن**")
         return 
     else:
         await message.reply_text("**رتبتك هي » العضو**")
