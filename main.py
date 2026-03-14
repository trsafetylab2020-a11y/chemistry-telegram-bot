import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

# حساب الادمن (انت)
ADMIN_USERS = [671598385]

# المستخدمين المشتركين
PAID_USERS = []

# رابط الدفع
PAYMENT_TEXT = """
💳 الاشتراك الكامل

فتح جميع فصول الكيمياء + الاختبارات + الملازم

السعر: 25,000 دينار

الدفع عبر كي كارد:

5556960115150247

بعد التحويل أرسل صورة التحويل إلى الإدارة.
"""

# القائمة الرئيسية
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [

        [InlineKeyboardButton("📘 الفصل الأول (مجاني)", callback_data="chapter1")],
        [InlineKeyboardButton("🔒 الفصل الثاني", callback_data="chapter2")],
        [InlineKeyboardButton("🔒 الفصل الثالث", callback_data="chapter3")],
        [InlineKeyboardButton("🔒 الفصل الرابع", callback_data="chapter4")],
        [InlineKeyboardButton("🔒 الفصل الخامس", callback_data="chapter5")],
        [InlineKeyboardButton("🔒 الفصل السادس", callback_data="chapter6")],

        [InlineKeyboardButton("📚 مكتبة الملازم", callback_data="library")],
        [InlineKeyboardButton("🎥 فيديوهات الشرح", callback_data="videos")],
        [InlineKeyboardButton("💳 الاشتراك", callback_data="subscribe")]

    ]

    await update.message.reply_text(
        "👋 أهلاً بك في منصة كيمياء السادس العلمي\nاختر ما تريد:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

# الفصل الاول
    if query.data == "chapter1":

        keyboard = [

            [InlineKeyboardButton("⚛️ تركيب الذرة", callback_data="lesson1")],
            [InlineKeyboardButton("📊 الجدول الدوري", callback_data="lesson2")],
            [InlineKeyboardButton("🔗 الروابط الكيميائية", callback_data="lesson3")],
            [InlineKeyboardButton("🧪 العناصر والمجموعات", callback_data="lesson4")],
            [InlineKeyboardButton("📈 الخواص الكيميائية", callback_data="lesson5")],
            [InlineKeyboardButton("🧠 اختبار الفصل", callback_data="test1")],

            [InlineKeyboardButton("⬅️ رجوع", callback_data="back")]

        ]

        await query.edit_message_text(
            "📘 الفصل الأول\nاختر الدرس:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# مثال شرح درس
    elif query.data == "lesson1":

        text = """
⚛️ تركيب الذرة

الذرة هي أصغر جزء من العنصر يحتفظ بخواصه الكيميائية.

تتكون الذرة من:

1- البروتونات (موجبة الشحنة)
2- النيوترونات (متعادلة)
3- الالكترونات (سالبة الشحنة)

توجد البروتونات والنيوترونات في النواة بينما تدور الالكترونات في مستويات طاقة حول النواة.

العدد الذري = عدد البروتونات
العدد الكتلي = بروتونات + نيوترونات
"""

        keyboard = [

            [InlineKeyboardButton("🎥 فيديو الشرح", url="https://youtube.com")],
            [InlineKeyboardButton("📚 مكتبة الملازم", callback_data="library")],
            [InlineKeyboardButton("⬅️ رجوع للدروس", callback_data="chapter1")]

        ]

        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# مكتبة الملازم
    elif query.data == "library":

        keyboard = [

            [InlineKeyboardButton(
                "📄 ملزمة الشرح الجزء الأول",
                url="https://drive.google.com/file/d/1vSK6SxkQRQl23aVR4RvZgpuUbHW0iUsT/view"
            )],

            [InlineKeyboardButton(
                "📄 ملزمة الشرح الجزء الثاني",
                url="https://drive.google.com/file/d/1uxzE2l43iLopD81axegAEY0iFVCeEJmq/view"
            )],

            [InlineKeyboardButton(
                "🧠 ملزمة الوزاريات",
                url="https://drive.google.com/file/d/15Y1Ozad8T3FEuu_Wc3hpR97dxjSTxvbQ/view"
            )],

            [InlineKeyboardButton(
                "📚 ملزمة إضافية",
                url="https://drive.google.com/file/d/1DqK6u1FMKq1i8Gba-zutF7xMMkpkieDQ/view"
            )],

            [InlineKeyboardButton(
                "🏫 ملزمة سنتر السادس",
                url="https://drive.google.com/file/d/1ERWeEwlGCDniBuZJ3zOM3tONLLD_Xi5g/view"
            )],

            [InlineKeyboardButton("⬅️ رجوع", callback_data="back")]

        ]

        await query.edit_message_text(
            "📚 مكتبة الملازم",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# فيديوهات
    elif query.data == "videos":

        keyboard = [

            [InlineKeyboardButton("🎥 شرح الفصل الأول", url="https://youtube.com")],
            [InlineKeyboardButton("🎥 شرح الفصل الثاني", url="https://youtube.com")],
            [InlineKeyboardButton("⬅️ رجوع", callback_data="back")]

        ]

        await query.edit_message_text(
            "🎥 فيديوهات شرح الكيمياء",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# الاشتراك
    elif query.data == "subscribe":

        await query.edit_message_text(PAYMENT_TEXT)

# رجوع
    elif query.data == "back":

        keyboard = [

            [InlineKeyboardButton("📘 الفصل الأول (مجاني)", callback_data="chapter1")],
            [InlineKeyboardButton("🔒 الفصل الثاني", callback_data="chapter2")],
            [InlineKeyboardButton("🔒 الفصل الثالث", callback_data="chapter3")],
            [InlineKeyboardButton("🔒 الفصل الرابع", callback_data="chapter4")],
            [InlineKeyboardButton("🔒 الفصل الخامس", callback_data="chapter5")],
            [InlineKeyboardButton("🔒 الفصل السادس", callback_data="chapter6")],

            [InlineKeyboardButton("📚 مكتبة الملازم", callback_data="library")],
            [InlineKeyboardButton("🎥 فيديوهات الشرح", callback_data="videos")],
            [InlineKeyboardButton("💳 الاشتراك", callback_data="subscribe")]

        ]

        await query.edit_message_text(
            "القائمة الرئيسية",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

app.run_polling()
