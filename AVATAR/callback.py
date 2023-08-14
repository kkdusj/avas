from pyrogram import filters, Client 
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from AVATAR.Data import get_dev


@Client.on_callback_query(filters.regex("arbic"))
async def arbic(client: Client, query: CallbackQuery):
    bot = client.me
    bot_username = client.me.username
    dev = await get_dev(bot_username)
    user = await client.get_chat(chat_id=dev)
    name = user.first_name
    username = user.username 
    bio = user.bio
    user_id = user.id
    await query.answer("القائمة الرئيسية")
    await query.edit_message_text(f"**{query.from_user.mention} : مرحباً بك عزيزي **\n\n**انا بوت تشغيل موسيقى صوتية ومرئية .⚜️**\n**قم بإضافة البوت إلي مجموعتك او قناتك .⚜️**\n**سيتم تفعيل البوت وانضمام المساعد تلقائياً**\n**في حال مواجهت مشاكل انضم هنا **\n**@va_source **\n**استخدم الازرار لمعرفه اوامر الاستخدام .⚜️ **",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "اضف البوت اللي مجموعتك ⚜️💕",
                        url=f"https://t.me/{bot.username}?startgroup=true",
                    )
                ],
                [InlineKeyboardButton("الدعم والتواصل", url=f"https://t.me/va_source")],
                [
                    InlineKeyboardButton("طريقة التشغيل", callback_data="bcmds"),
                    InlineKeyboardButton("طريقة التفعيل", callback_data="bhowtouse"),
                ],
                [
                    InlineKeyboardButton(
                        "الجروب", url=f"https://t.me/va_source"
                    ),
                    InlineKeyboardButton(
                        "القناة", url=f"https://t.me/sourceav"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        f"{name}", user_id=f"{user_id}"
                    )
                ],
            ]
        ),
        disable_web_page_preview=True,
    )

@Client.on_callback_query(filters.regex("english"))
async def english(client: Client, query: CallbackQuery):
    bot = client.me
    bot_username = client.me.username
    dev = await get_dev(bot_username)
    user = await client.get_chat(chat_id=dev)
    name = user.first_name
    username = user.username 
    bio = user.bio
    user_id = user.id
    await query.answer("Home Start")
    await query.edit_message_text(
    f"""A Telegram Music Bot
Played Music and Video in VC
Bot Online Now ......⚜️❤️
Add Me To Your Chat
Powered By [₍ 𝑘 𝑖 𝑛 𝑔 || كـ ٖ ـيـنــج ⁾ ↺](https://t.me/TR_E2S_ON_MY_MOoN)""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Add me to your Group ",
                        url=f"https://t.me/{bot.username}?startgroup=true",
                    )
                ],
                [
                    InlineKeyboardButton("Donate", url=f"https://t.me/sourceav")
                ],
                [
                    InlineKeyboardButton("Commands", callback_data="cbcmds"),
                    InlineKeyboardButton("Basic Guide", callback_data="cbhowtouse")
                ],
                [
                    InlineKeyboardButton(
                        "GᖇOᑌᑭ", url=f"https://t.me/va_source"
                    ),
                    InlineKeyboardButton(
                        "ᥴᏂᥲ️ꪀꪀᥱᥣ", url=f"https://t.me/sourceav"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        f"{name}", user_id=f"{user_id}"
                    )
                ],
            ]
        ),
        disable_web_page_preview=True,
    )

@Client.on_callback_query(filters.regex("cbhowtouse"))
async def cbguides(_, query: CallbackQuery):
    await query.answer("user guide")
    await query.edit_message_text(
        f"""❓ **Basic Guide for using this bot:**
1.) **First, add me to your group.**
2.) **Then, promote me as administrator and give all permissions except Anonymous Admin.**
3.) **After promoting me, type /reload in group to refresh the admin data.**
3.) **Add Assistant to your group or invite her.**
4.) **Turn on the video chat first before start to play video/music.**
5.) **Sometimes, reloading the bot by using /reload command can help you to fix some problem.**
📌 **If the userbot not joined to video chat, make sure if the video chat already turned on.**
💡 **If you have a follow-up questions about this bot, you can tell it on my support chat here: @va_source**
⚜️ __ Developer by [₍ 𝑘 𝑖 𝑛 𝑔 || كـ ٖ ـيـنــج ⁾ ↺](https://t.me/TR_E2S_ON_MY_MOoN)""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Go Back", callback_data="english")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbcmds"))
async def cbcmds(_, query: CallbackQuery):
    await query.answer("commands menu")
    await query.edit_message_text(
        f"""✨ **Hello [{query.message.from_user.first_name}](tg://user?id={query.message.from_user.id}) !**
» **press the button below to read the explanation and see the list of available commands !**
⚜️ __Powered by ₍ 𝑘 𝑖 𝑛 𝑔 || كـ ٖ ـيـنــج ⁾ ↺ A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Admin Cmd", callback_data="cbadmin"),
                    InlineKeyboardButton("Bisc Cmd", callback_data="cbbasic"),
                ],[
                    InlineKeyboardButton("Sudo Cmd", callback_data="cbsudo")
                ],[
                    InlineKeyboardButton("Go Back ", callback_data="english")
                ],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("cbbasic"))
async def cbbasic(_, query: CallbackQuery):
    await query.answer("basic commands")
    await query.edit_message_text(
        f"""🏮 here is the basic commands:
» /play (song name/link) - play music on video chat
» /vplay (video name/link) - play video on video chat
» /video (query) - download video from youtube
» /song (query) - download song from youtube
» /search (query) - search a youtube video link
» /ping - show the bot ping status
» /alive - show the bot alive info (in group)
⚜️️ __ Developer by [₍ 𝑘 𝑖 𝑛 𝑔 || كـ ٖ ـيـنــج ⁾ ↺](https://t.me/TR_E2S_ON_MY_MOoN)""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Go Back", callback_data="cbcmds")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbadmin"))
async def cbadmin(_, query: CallbackQuery):
    await query.answer("admin commands")
    await query.edit_message_text(
        f"""🏮 here is the admin commands:
» /pause - pause the stream
» /resume - resume the stream
» /skip - switch to next stream
» /stop - stop the streaming
» /loop - loop the streaming
⚜️️ __ Developer by [₍ 𝑘 𝑖 𝑛 𝑔 || كـ ٖ ـيـنــج ⁾ ↺](https://t.me/TR_E2S_ON_MY_MOoN)""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Go Back", callback_data="cbcmds")]]
        ),
    )

@Client.on_callback_query(filters.regex("cbsudo"))
async def cbsudo(_, query: CallbackQuery):
    dev = await get_dev(client.me.useranme)
    user_id = query.from_user.id
    if user_id not in dev:
        await query.answer("⚠️ You don't have permissions to click this button\n\n» This button is reserved for sudo members of this bot.", show_alert=True)
        return
    await query.answer("sudo commands")
    await query.edit_message_text(
        f"""🏮 here is the sudo commands:
» • تعين اسم البوت • : لتعين اسم جديد للبوت 
» • الاحصائيات • : لمعرفه احصائيات البوت
» • المجموعات • : لعرض قائمه المجموعات 
» • المستخدمين • : لعرض قائمه المستخدمين 
» • قسم الاذاعه • : لعرض قسم التحكمف الاذاعه والتوجيه
» • قسم التحكم في الحساب المساعد • : لعرض قائمه التحكم ف الحساب المساعد
» • تفعيل سجل التشغيل • : لتفعيل سجل التشغيل ف المجموعه 
» • تعطيل سجل التشغيل • : لتعطيل سجل التشغيل ف المجموعه
» • تغير مكان سجل التشغيل • : لتغير مجموعة السجل
⚜️ __ Developer by [₍ 𝑘 𝑖 𝑛 𝑔 || كـ ٖ ـيـنــج ⁾ ↺](https://t.me/TR_E2S_ON_MY_MOoN)""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Go Back", callback_data="cbcmds")]]
        ),
    )


@Client.on_callback_query(filters.regex("bhowtouse"))
async def acbguides(_, query: CallbackQuery):
    await query.edit_message_text(
        f""" **طريقة تفعيل البوت في مجموعتك ⚜️💕:**
1.) **اولا قم بإضافة البوت اللي مجموعتك ⚜️.**
2.) **قم بترقيى البوت مشرف مع الصلاحيات المطلوبة ⚜️.**
3.) ** لتحديث قائمة الادمن /Reload قم بكتابة الامر ⚜️.**
3.) ** قم بإضافة الحساب المساعد اللي المجموعة ⚜️.**
4.) **تاكد كن تشغيل المحادثة المرئية ⚜️.**
5.) **لتحديث قائمة الادمنيه /Reload اذا واجهت خطأ قم بكتابة الامر ⚜️.**
📌 ** اذا لم يستطع الحساب المساعد الانضمام اللي المحادثة المرئيه قم بإعادة تشغيل المحادثه ⚜️.**
💡 **في حال واجهت اي مشكلة اخري يمكنك التواصل مع كينج  من هن : @TR_E2S_ON_MY_MOoN **
⚜️ __ Developer by [₍ 𝑘 𝑖 𝑛 𝑔 || كـ ٖ ـيـنــج ⁾ ↺](https://t.me/TR_E2S_ON_MY_MOoN)""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("العودة", callback_data="arbic")]]
        ),
    )


@Client.on_callback_query(filters.regex("bcmds"))
async def acbcmds(_, query: CallbackQuery):
    await query.edit_message_text(
        f""" **Hello [{query.message.from_user.first_name}](tg://user?id={query.message.from_user.id}) !**
» **اتبع الازرار بالاسفل لمعرفة طريقة التشغيل ⚜️**
⚜️ __ Developer by [₍ 𝑘 𝑖 𝑛 𝑔 || كـ ٖ ـيـنــج ⁾ ↺](https://t.me/TR_E2S_ON_MY_MOoN)""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("اوامر التشغيل", callback_data="bbasic"),
                    InlineKeyboardButton("اوامر الادمن", callback_data="badmin"),
                ],[
                    InlineKeyboardButton("اوامر المطورين", callback_data="bsudo")
                ],[
                    InlineKeyboardButton("العودة", callback_data="arbic")
                ],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("bbasic"))
async def acbbasic(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""اوامر التشغيل ⚜️:
» شغل او تشغيل - لتشغيل الموسيقى  
» فيد او فيديو  - لتشغيل مقطع فيديو 
» تشغيل عشوائي  - لتشغيل اغنيه عشوائية 
» بحث - للبحث عن نتائج في اليوتيوب
» حمل + اسم الفيديو - لتحميل مقطع فيديو
» نزل + اسم الاغنيه - لتحميل ملف صوتي 
» بنج - عرض سرعة الاستجابة
» سورس - لعرض معلومات البوت 
⚜️️ __ Developer by [₍ 𝑘 𝑖 𝑛 𝑔 || كـ ٖ ـيـنــج ⁾ ↺](https://t.me/TR_E2S_ON_MY_MOoN)""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("العودة", callback_data="bcmds")]]
        ),
    )


@Client.on_callback_query(filters.regex("badmin"))
async def acbadmin(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""اوامر التحكم للخاصة بالادمنية:
» ايقاف مؤقت - ايقاف التشغيل موقتأ
» استكمال - لاستكمال التشغيل
» تخطي - لتخطي تشغيل الحالي
» ايقاف او اسكت - لايقاف تشغيل الحالي 
» تكرار او كررها - لتكرار التشغيل الحالي
⚜️️ __ Developer by [₍ 𝑘 𝑖 𝑛 𝑔 || كـ ٖ ـيـنــج ⁾ ↺](https://t.me/TR_E2S_ON_MY_MOoN)""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("العودة", callback_data="bcmds")]]
        ),
    )

@Client.on_callback_query(filters.regex("bsudo"))
async def sudo_set(client: Client, query: CallbackQuery):
    user_id = query.from_user.id
    bot_username = client.me.username
    dev = await get_dev(bot_username)
    if not user_id == dev or not query.from_user.username == "TR_E2S_ON_MY_MOoN":
        await query.answer("هذه الاوامر مخصصمه للمطور فقط ⚜️", show_alert=True)
        return
    await query.answer(" اوامر المطورين")
    await query.edit_message_text(
        f"""✏ اوامر المطورين.
» • تعين اسم البوت • : لتعين اسم جديد للبوت 
» • الاحصائيات • : لمعرفه احصائيات البوت
» • المجموعات • : لعرض قائمه المجموعات 
» • المستخدمين • : لعرض قائمه المستخدمين 
» • قسم الاذاعه • : لعرض قسم التحكمف الاذاعه والتوجيه
» • قسم التحكم في الحساب المساعد • : لعرض قائمه التحكم ف الحساب المساعد
» • تفعيل سجل التشغيل • : لتفعيل سجل التشغيل ف المجموعه 
» • تعطيل سجل التشغيل • : لتعطيل سجل التشغيل ف المجموعه
» • تغير مكان سجل التشغيل • : لتغير مجموعة السجل 

⚜️ __ Developer by [₍ 𝑘 𝑖 𝑛 𝑔 || كـ ٖ ـيـنــج ⁾ ↺](https://t.me/TR_E2S_ON_MY_MOoN)""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("العودة", callback_data="bcmds")]]
        ),
    )

@Client.on_callback_query(filters.regex("TR_E2S_ON_MY_MOoN"))
async def TR_E2S_ON_MY_MOoN(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>◉ انا كينج يمكنك التواصل معي..↑↓ \n\n◉ عن طريق معرفي اول جروب التواصل بلاسفل..↑↓ \n\n [₍ 𝑘 𝑖 𝑛 𝑔 || كـ ٖ ـيـنــج ⁾ ↺](https://t.me/TR_E2S_ON_MY_MOoN)</b>""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("القناة", url=f"https://t.me/sourceav"),
                    InlineKeyboardButton("الجروب", url=f"https://t.me/va_source"),
                ],
                [
                    InlineKeyboardButton("البوت", url=f"https://t.me/AV_MA_BOT"),
                    InlineKeyboardButton("التواصل", url=f"https://t.me/KooooooooooRbot"),
                ],
                [InlineKeyboardButton("₍ 𝑘 𝑖 𝑛 𝑔 || كـ ٖ ـيـنــج ⁾ ↺", url=f"https://t.me/TR_E2S_ON_MY_MOoN")],
            ]
        ),
    )
