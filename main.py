import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

ADMIN = 671598385

paid_users = []
scores = {}

KI_CARD = "5556960115150247"


# ===============================
# القائمة الرئيسية
# ===============================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [

        [InlineKeyboardButton("📘 الفصل الأول", callback_data="ch1")],
        [InlineKeyboardButton("🔒 الفصل الثاني", callback_data="locked")],
        [InlineKeyboardButton("🔒 الفصل الثالث", callback_data="locked")],
        [InlineKeyboardButton("🔒 الفصل الرابع", callback_data="locked")],
        [InlineKeyboardButton("🔒 الفصل الخامس", callback_data="locked")],
        [InlineKeyboardButton("🔒 الفصل السادس", callback_data="locked")],

        [InlineKeyboardButton("🎥 فيديوهات الشرح", callback_data="videos")],
        [InlineKeyboardButton("📚 مكتبة الملازم", callback_data="library")],
        [InlineKeyboardButton("🧠 الاختبارات", callback_data="tests")],
        [InlineKeyboardButton("📊 درجاتي", callback_data="myscore")],
        [InlineKeyboardButton("💳 الاشتراك", callback_data="subscribe")]

    ]

    await update.message.reply_text(
        "📚 منصة كيمياء السادس العلمي\nاختر من القائمة:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ===============================
# الأزرار
# ===============================

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    user = query.from_user.id
    await query.answer()


# ===============================
# الفصل الاول
# ===============================

    if query.data == "ch1":

        keyboard = [

            [InlineKeyboardButton("⚛️ تركيب الذرة", callback_data="atom")],
            [InlineKeyboardButton("📊 الجدول الدوري", callback_data="periodic")],
            [InlineKeyboardButton("🧠 اختبار الفصل", callback_data="test1")],

            [InlineKeyboardButton("⬅️ رجوع", callback_data="back")]

        ]

        await query.edit_message_text(
            "📘 الفصل الأول",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


# ===============================
# درس الذرة
# ===============================

    elif query.data == "atom":

        text = """
⚛️ تركيب الذرة

الذرة أصغر جزء من العنصر يحتفظ بخواصه الكيميائية.

تتكون الذرة من:

• بروتونات موجبة
• نيوترونات متعادلة
• إلكترونات سالبة

العدد الذري = عدد البروتونات
العدد الكتلي = بروتونات + نيوترونات
"""

        keyboard = [

            [InlineKeyboardButton(
                "🎥 فيديو الشرح",
                url="https://www.youtube.com/watch?v=Nh9yq3cOVsY"
            )],

            [InlineKeyboardButton(
                "📚 تحميل الملزمة",
                callback_data="library"
            )],

            [InlineKeyboardButton(
                "🧠 أسئلة وزارية",
                callback_data="q_atom"
            )],

            [InlineKeyboardButton(
                "⬅️ رجوع",
                callback_data="ch1"
            )]

        ]

        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


# ===============================
# سؤال وزاري
# ===============================

    elif query.data == "q_atom":

        keyboard = [

            [InlineKeyboardButton("عدد البروتونات", callback_data="a1")],
            [InlineKeyboardButton("عدد الالكترونات", callback_data="a2")],
            [InlineKeyboardButton("عدد النيوترونات", callback_data="a3")],
            [InlineKeyboardButton("العدد الكتلي", callback_data="a4")]

        ]

        await query.edit_message_text(
            "سؤال وزاري 2019\n\nما المقصود بالعدد الذري؟",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


    elif query.data == "a1":

        scores[user] = scores.get(user,0)+1

        await query.edit_message_text(
            "✅ إجابة صحيحة\nالدرجة +1"
        )

    elif query.data in ["a2","a3","a4"]:

        await query.edit_message_text(
            "❌ إجابة خاطئة\nالإجابة الصحيحة: عدد البروتونات"
        )


# ===============================
# الاختبار
# ===============================

    elif query.data == "test1":

        keyboard = [

            [InlineKeyboardButton("عدد البروتونات", callback_data="t1")],
            [InlineKeyboardButton("عدد الالكترونات", callback_data="t2")],
            [InlineKeyboardButton("عدد النيوترونات", callback_data="t3")]

        ]

        await query.edit_message_text(
            "اختبار الفصل الأول\n\nما العدد الذري؟",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


    elif query.data == "t1":

        scores[user] = scores.get(user,0)+1

        await query.edit_message_text(
            "✅ صحيح\nالدرجة +1"
        )


# ===============================
# الدرجات
# ===============================

    elif query.data == "myscore":

        s = scores.get(user,0)

        await query.edit_message_text(
            f"📊 مجموع درجاتك\n{s}"
        )


# ===============================
# الملازم
# ===============================

    elif query.data == "library":

        keyboard = [

            [InlineKeyboardButton(
                "📄 ملزمة الجزء الأول",
                url="https://drive.google.com/file/d/1vSK6SxkQRQl23aVR4RvZgpuUbHW0iUsT/view"
            )],

            [InlineKeyboardButton(
                "📄 ملزمة الجزء الثاني",
                url="https://drive.google.com/file/d/1uxzE2l43iLopD81axegAEY0iFVCeEJmq/view"
            )],

            [InlineKeyboardButton(
                "📄 الوزاريات",
                url="https://drive.google.com/file/d/15Y1Ozad8T3FEuu_Wc3hpR97dxjSTxvbQ/view"
            )],

            [InlineKeyboardButton("⬅️ رجوع", callback_data="back")]

        ]

        await query.edit_message_text(
            "📚 مكتبة الملازم",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


# ===============================
# الاشتراك
# ===============================

    elif query.data == "subscribe":

        await query.edit_message_text(
f"""
💳 الاشتراك الكامل

السعر: 25,000 دينار

الدفع عبر كي كارد:

{KI_CARD}

بعد التحويل أرسل صورة الدفع للإدارة.
"""
        )


# ===============================
# رجوع
# ===============================

    elif query.data == "back":

        keyboard = [

        [InlineKeyboardButton("📘 الفصل الأول", callback_data="ch1")],
        [InlineKeyboardButton("🔒 الفصل الثاني", callback_data="locked")],
        [InlineKeyboardButton("🔒 الفصل الثالث", callback_data="locked")],
        [InlineKeyboardButton("🔒 الفصل الرابع", callback_data="locked")],
        [InlineKeyboardButton("🔒 الفصل الخامس", callback_data="locked")],
        [InlineKeyboardButton("🔒 الفصل السادس", callback_data="locked")],

        [InlineKeyboardButton("🎥 فيديوهات الشرح", callback_data="videos")],
        [InlineKeyboardButton("📚 مكتبة الملازم", callback_data="library")],
        [InlineKeyboardButton("🧠 الاختبارات", callback_data="tests")],
        [InlineKeyboardButton("📊 درجاتي", callback_data="myscore")],
        [InlineKeyboardButton("💳 الاشتراك", callback_data="subscribe")]

        ]

        await query.edit_message_text(
            "القائمة الرئيسية",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


# ===============================
# تشغيل البوت
# ===============================

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))

app.run_polling()
