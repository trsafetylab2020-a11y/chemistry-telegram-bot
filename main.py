import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

# قراءة التوكن من Secrets
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# معرفات الحسابات المجانية (أنت وابنك)
ADMIN_USERS = [123456789]  # ضع معرف Telegram الخاص بك هنا

# قائمة الطلاب المدفوعين (للفصول المقفلة)
PAID_USERS = []

# ======= دروس الفصل الأول =======
LESSONS_CHAPTER1 = {
    "lesson1": {
        "title": "تركيب الذرة",
        "content": """📘 الدرس 1: تركيب الذرة

- الذرة تتكون من البروتون (+)، النيوترون (0)، الإلكترون (-)
- العدد الذري = عدد البروتونات = عدد الإلكترونات
- مثال: Na → Z = 11 → 11 بروتون و11 إلكترون"""
    },
    "lesson2": {
        "title": "الجدول الدوري",
        "content": """📘 الدرس 2: الجدول الدوري

- ترتيب العناصر حسب العدد الذري
- العناصر في نفس المجموعة لها نفس عدد إلكترونات التكافؤ
- خصائص متشابهة بين عناصر كل مجموعة"""
    },
    "lesson3": {
        "title": "الروابط الكيميائية",
        "content": """📘 الدرس 3: الروابط الكيميائية

- الروابط الأيونية: انتقال إلكترونات بين الذرات
- الروابط التساهمية: مشاركة الإلكترونات بين الذرات
- الروابط المعدنية: إلكترونات حرة بين ذرات المعدن"""
    },
    "lesson4": {
        "title": "العناصر والمجموعات",
        "content": """📘 الدرس 4: العناصر والمجموعات

- المجموعات الرأسية → خصائص متشابهة
- الدورات الأفقية → زيادة العدد الذري
- أمثلة على خصائص الفلزات واللافلزات"""
    },
    "lesson5": {
        "title": "الخواص الكيميائية والفيزيائية",
        "content": """📘 الدرس 5: الخواص الكيميائية والفيزيائية

- الخواص الفيزيائية: الكثافة، الذوبان، درجة الغليان، اللون
- الخواص الكيميائية: التفاعل مع الأحماض، القواعد، الأكسجين"""
    }
}

# ======= أسئلة وزارية للفصل الأول (2020-2026) =======
QUESTIONS_CHAPTER1 = [
    {"question": "ما المقصود بالعدد الذري؟",
     "options": ["عدد النيوترونات", "عدد البروتونات", "عدد المدارات", "عدد الإلكترونات فقط"],
     "answer": "عدد البروتونات", "year": 2021},
    
    {"question": "كم عدد إلكترونات ذرة الصوديوم؟",
     "options": ["10", "11", "12", "23"],
     "answer": "11", "year": 2020},
    
    {"question": "أي الجسيمات التالية موجبة الشحنة؟",
     "options": ["الإلكترون", "البروتون", "النيوترون", "المدار"],
     "answer": "البروتون", "year": 2024},
    
    {"question": "ما سبب تشابه عناصر المجموعة الواحدة في الجدول الدوري؟",
     "options": ["عدد الإلكترونات الكلي", "عدد الإلكترونات الخارجية", "عدد النيوترونات", "عدد المدارات"],
     "answer": "عدد الإلكترونات الخارجية", "year": 2023},
    
    {"question": "ما نوع الرابط بين ذرتي هيدروجين في H2؟",
     "options": ["أيونية", "تساهمية", "فلزية", "هيدروجينية"],
     "answer": "تساهمية", "year": 2021},
    
    {"question": "ما الخاصية الفيزيائية التي تحدد إذا كان العنصر صلباً أم سائلاً؟",
     "options": ["درجة الغليان", "العدد الذري", "عدد الإلكترونات", "نوع الرابط"],
     "answer": "درجة الغليان", "year": 2020},
    
    {"question": "أي الجسيمات التالية متعادلة كهربائياً؟",
     "options": ["الإلكترون", "البروتون", "النيوترون", "المدار"],
     "answer": "النيوترون", "year": 2022},
]

# ======= دالة start لعرض الفصول =======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📘 الفصل الأول (مجاني)", callback_data='chapter1')],
        [InlineKeyboardButton("🔒 الفصل الثاني", callback_data='chapter2')],
        [InlineKeyboardButton("🔒 الفصل الثالث", callback_data='chapter3')],
        [InlineKeyboardButton("🔒 الفصل الرابع", callback_data='chapter4')],
        [InlineKeyboardButton("🔒 الفصل الخامس", callback_data='chapter5')],
        [InlineKeyboardButton("🔒 الفصل السادس", callback_data='chapter6')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "اهلا بك في منصة الكيمياء السادس العلمي\nاختر الفصل الذي تريد:", 
        reply_markup=reply_markup
    )

# ======= دالة button لمعالجة الضغط =======
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    # ===== الفصل الأول مجاني =====
    if query.data == 'chapter1':
        keyboard = [
            [InlineKeyboardButton(lesson["title"], callback_data=key)]
            for key, lesson in LESSONS_CHAPTER1.items()
        ]
        keyboard.append([InlineKeyboardButton("📝 اختبار الفصل", callback_data='test_chapter1')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "📘 الفصل الأول\nاختر الدرس أو الاختبار:", 
            reply_markup=reply_markup
        )

    # عرض محتوى الدروس
    elif query.data.startswith("lesson"):
        lesson = LESSONS_CHAPTER1.get(query.data)
        if lesson:
            await query.edit_message_text(f"📖 {lesson['title']}\n\n{lesson['content']}")

    # اختبار الفصل الأول
    elif query.data == 'test_chapter1':
        text = "📝 اختبار الفصل الأول (أسئلة وزارية)\n\n"
        for i, q in enumerate(QUESTIONS_CHAPTER1, start=1):
            text += f"السؤال {i} (وزاري {q['year']}): {q['question']}\n"
            for j, opt in enumerate(q['options'], start=1):
                text += f"{j}. {opt}\n"
            text += "\n"
        await query.edit_message_text(text)

    # الفصول المقفلة
    elif query.data.startswith('chapter'):
        if user_id in ADMIN_USERS or user_id in PAID_USERS:
            await query.edit_message_text(f"📘 {query.data} محتوى الفصل متاح لك الآن")
        else:
            keyboard = [[InlineKeyboardButton("💳 الدفع عبر Ki‑Card / ZainCash", url="https://your-payment-link.com")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text("🔒 هذا الفصل متاح بعد الاشتراك", reply_markup=reply_markup)

# ===== إنشاء البوت وتشغيله =====
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.run_polling()
