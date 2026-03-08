import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

# قراءة التوكن من Secrets
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# معرفات الحسابات المجانية (أنت وابنك)
ADMIN_USERS = [123456789]  # ضع معرف Telegram الخاص بك هنا

# قائمة الطلاب المدفوعين (للفصول المقفلة)
PAID_USERS = []

# ======= دروس الفصل الأول (شرح مفصل لكل درس) =======
LESSONS_CHAPTER1 = {
    "lesson1": {
        "title": "تركيب الذرة",
        "content": """
📘 الدرس 1: تركيب الذرة (شرح كامل)

1. مقدمة:
الذرة هي أصغر وحدة من المادة تحتفظ بخواص العنصر، وتتكون من نواة وإلكترونات تتحرك حولها.

2. النواة:
- تحتوي على البروتونات (+) والنيوترونات (0)
- البروتونات تحدد العدد الذري Z
- النيوترونات تحدد الكتلة الذرية تقريباً

3. الإلكترونات:
- تدور حول النواة في مستويات الطاقة
- عدد الإلكترونات = عدد البروتونات في الذرة المتعادلة
- الإلكترونات الخارجية تحدد خواص العنصر الكيميائية

4. التوزيع الإلكتروني:
- الإلكترونات توزع في مستويات الطاقة حسب قاعدة Aufbau
- مثال: Na → 1s² 2s² 2p⁶ 3s¹

5. أمثلة وتمارين محلولة:
- ذرة الأكسجين O: Z = 8 → 8 بروتون، 8 إلكترون
- ذرة الكربون C: Z = 6 → 6 بروتون، 6 إلكترون
"""
    },
    "lesson2": {
        "title": "الجدول الدوري",
        "content": """
📘 الدرس 2: الجدول الدوري (شرح كامل)

1. ترتيب العناصر:
- العناصر مرتبة حسب العدد الذري (Z)
- كل صف أفقي يسمى دورة
- كل عمود عمودي يسمى مجموعة

2. خصائص المجموعات:
- العناصر في نفس المجموعة لها نفس عدد إلكترونات التكافؤ
- أمثلة: مجموعة الفلزات القلوية → Li, Na, K

3. خصائص الدورات:
- العدد الذري يزيد من اليسار إلى اليمين
- الخصائص الكيميائية تتغير تدريجياً

4. استخدام الجدول الدوري:
- التنبؤ بخصائص العناصر
- معرفة الروابط الكيميائية المحتملة
"""
    },
    "lesson3": {
        "title": "الروابط الكيميائية",
        "content": """
📘 الدرس 3: الروابط الكيميائية (شرح كامل)

1. الروابط الأيونية:
- انتقال الإلكترونات من ذرة إلى أخرى
- مثال: NaCl → Na⁺ + Cl⁻

2. الروابط التساهمية:
- مشاركة الإلكترونات بين الذرات
- مثال: H2O → كل H يشارك إلكترون مع O

3. الروابط المعدنية:
- إلكترونات حرة تتحرك بين ذرات المعدن
- تعطي المعادن خاصية التوصيل الكهربائي

4. الروابط الهيدروجينية:
- تفاعل بين هيدروجين مرتبط بذرة كهربية عالية (O, N, F)
- موجودة في الماء، DNA
"""
    },
    "lesson4": {
        "title": "العناصر والمجموعات",
        "content": """
📘 الدرس 4: العناصر والمجموعات (شرح كامل)

1. المجموعات الرأسية:
- عناصر بنفس الخصائص الكيميائية
- عدد إلكترونات التكافؤ متشابه

2. الدورات الأفقية:
- ترتيب العناصر حسب العدد الذري
- خصائص العناصر تتغير تدريجياً

3. أمثلة:
- الفلزات → توصيل كهرباء، لامعة
- اللافلزات → عازلة، غير لامعة
- أشباه الفلزات → خصائص وسطية
"""
    },
    "lesson5": {
        "title": "الخواص الكيميائية والفيزيائية",
        "content": """
📘 الدرس 5: الخواص الكيميائية والفيزيائية (شرح كامل)

1. الخواص الفيزيائية:
- الكثافة، الذوبان، درجة الغليان، اللون
- يمكن قياسها بدون تغيير تركيب المادة

2. الخواص الكيميائية:
- كيفية تفاعل العنصر مع الأحماض، القواعد، الأكسجين
- تؤدي إلى تغير في تركيب المادة

3. أمثلة محلولة:
- الحديد يتفاعل مع الأكسجين → صدأ
- الماء يغلي عند 100°C
"""
    }
}

# ======= أسئلة وزارية للفصل الأول (2020-2026) =======
QUESTIONS_CHAPTER1 = [
    {"question": "ما المقصود بالعدد الذري؟", "options": ["عدد النيوترونات", "عدد البروتونات", "عدد المدارات", "عدد الإلكترونات فقط"], "answer": "عدد البروتونات", "year": 2021},
    {"question": "كم عدد إلكترونات ذرة الصوديوم؟", "options": ["10", "11", "12", "23"], "answer": "11", "year": 2020},
    {"question": "أي الجسيمات التالية موجبة الشحنة؟", "options": ["الإلكترون", "البروتون", "النيوترون", "المدار"], "answer": "البروتون", "year": 2024},
    {"question": "ما سبب تشابه عناصر المجموعة الواحدة في الجدول الدوري؟", "options": ["عدد الإلكترونات الكلي", "عدد الإلكترونات الخارجية", "عدد النيوترونات", "عدد المدارات"], "answer": "عدد الإلكترونات الخارجية", "year": 2023},
    {"question": "ما نوع الرابط بين ذرتي هيدروجين في H2؟", "options": ["أيونية", "تساهمية", "فلزية", "هيدروجينية"], "answer": "تساهمية", "year": 2021},
    {"question": "ما الخاصية الفيزيائية التي تحدد إذا كان العنصر صلباً أم سائلاً؟", "options": ["درجة الغليان", "العدد الذري", "عدد الإلكترونات", "نوع الرابط"], "answer": "درجة الغليان", "year": 2020},
    {"question": "أي الجسيمات التالية متعادلة كهربائياً؟", "options": ["الإلكترون", "البروتون", "النيوترون", "المدار"], "answer": "النيوترون", "year": 2022},
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

    # الفصل الأول مجاني
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
            # تقسيم الرسائل الطويلة (>4000 حرف) إذا لزم
            content = f"📖 {lesson['title']}\n\n{lesson['content']}"
            if len(content) > 4000:
                chunks = [content[i:i+4000] for i in range(0, len(content), 4000)]
                for chunk in chunks:
                    await query.message.reply_text(chunk)
            else:
                await query.edit_message_text(content)

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
