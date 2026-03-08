import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

# قراءة التوكن من Environment Variables
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# معرفات الحسابات المجانية (أنت وابنك)
ADMIN_USERS = [123456789]  # ضع معرف Telegram الخاص بك هنا

# قائمة الطلاب المدفوعين (للفصول المقفلة)
PAID_USERS = []

# ======= دروس الفصل الأول (شرح شامل + أمثلة محلولة) =======
LESSONS_CHAPTER1 = {
    "lesson1": {
        "title": "تركيب الذرة",
        "content": """
📘 درس 1: تركيب الذرة

1. تعريف الذرة:
- أصغر وحدة من المادة تحتفظ بخواص العنصر.

2. مكونات الذرة:
أ. النواة: تحتوي على البروتونات (+) والنيوترونات (0)
- البروتونات تحدد العدد الذري Z
- النيوترونات تحدد الكتلة الذرية تقريباً

ب. الإلكترونات:
- تدور حول النواة في مستويات الطاقة
- عدد الإلكترونات = عدد البروتونات في الذرة المتعادلة
- الإلكترونات الخارجية تحدد خواص العنصر الكيميائية

3. مستويات الطاقة والإلكترونات:
- 1s, 2s, 2p, 3s...
- قاعدة Aufbau للترتيب
- مثال: Na → 1s² 2s² 2p⁶ 3s¹

4. أمثلة محلولة:
- ذرة الأكسجين O: Z=8 → 8 بروتون و8 إلكترون
- ذرة الكربون C: Z=6 → 6 بروتون و6 إلكترون

5. ملخص:
- البروتون = موجب
- النيوترون = متعادل
- الإلكترون = سالب
"""
    },
    "lesson2": {
        "title": "الجدول الدوري",
        "content": """
📘 درس 2: الجدول الدوري

1. ترتيب العناصر:
- حسب العدد الذري Z
- الصفوف = دورات، الأعمدة = مجموعات

2. خصائص المجموعات:
- نفس عدد إلكترونات التكافؤ
- مثال: مجموعة الفلزات القلوية → Li, Na, K

3. خصائص الدورات:
- التغير التدريجي للخواص الكيميائية
- العدد الذري يزيد من اليسار لليمين

4. استخدام الجدول الدوري:
- التنبؤ بخصائص العناصر
- معرفة نوع الروابط الكيميائية المحتملة

5. أمثلة محلولة:
- الصوديوم Na → فلز قلوي، تفاعل مع الماء
- الكلور Cl → غاز سام، يندمج بسهولة مع الفلزات

6. ملخص:
- المجموعات = خصائص متشابهة
- الدورات = تغير تدريجي للخصائص
"""
    },
    "lesson3": {
        "title": "الروابط الكيميائية",
        "content": """
📘 درس 3: الروابط الكيميائية

1. الروابط الأيونية:
- انتقال إلكترونات من ذرة لأخرى
- مثال: NaCl → Na⁺ + Cl⁻

2. الروابط التساهمية:
- مشاركة الإلكترونات بين ذرتين
- مثال: H2O → كل H يشارك إلكترون مع O

3. الروابط المعدنية:
- إلكترونات حرة تتحرك بين ذرات المعدن
- تعطي المعادن التوصيل الكهربائي واللمعان

4. الروابط الهيدروجينية:
- تفاعل بين هيدروجين مرتبط بذرة كهربية عالية (O, N, F)
- موجودة في الماء وDNA

5. أمثلة محلولة:
- H2 → تساهمي
- NaCl → أيوني
- Cu → فلزي

6. ملخص:
- أيوني → انتقال
- تساهمي → مشاركة
- فلزي → إلكترونات حرة
- هيدروجيني → تفاعل H مع O/N/F
"""
    },
    "lesson4": {
        "title": "العناصر والمجموعات",
        "content": """
📘 درس 4: العناصر والمجموعات

1. المجموعات الرأسية:
- خصائص كيميائية متشابهة
- عدد إلكترونات التكافؤ نفسه

2. الدورات الأفقية:
- ترتيب حسب العدد الذري
- التغير التدريجي للخصائص

3. أنواع العناصر:
- الفلزات → توصيل كهرباء، لامعة، قابلة للسحب والطرق
- اللافلزات → عازلة، غير لامعة
- أشباه الفلزات → خصائص وسطية

4. أمثلة محلولة:
- Na → فلز قلوي، تفاعل سريع مع الماء
- Cl → غاز سام، ينتمي لللافلزات
- Si → شبه فلز

5. ملخص:
- المجموعات → خصائص مشابهة
- الدورات → خصائص متدرجة
"""
    },
    "lesson5": {
        "title": "الخواص الكيميائية والفيزيائية",
        "content": """
📘 درس 5: الخواص الكيميائية والفيزيائية

1. الخواص الفيزيائية:
- الكثافة، الذوبان، درجة الغليان، اللون
- لا تغير تركيب المادة

2. الخواص الكيميائية:
- تفاعل العنصر مع الأحماض، القواعد، الأكسجين
- تغير تركيب المادة

3. أمثلة محلولة:
- الحديد + الأكسجين → صدأ
- الماء يغلي عند 100°C
- الصوديوم + الماء → NaOH + H2

4. ملخص:
- الفيزيائية → قياس بدون تغيير التركيب
- الكيميائية → تؤدي لتغيير التركيب
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

    # العودة للفصول
    if query.data == 'start_menu':
        keyboard = [
            [InlineKeyboardButton("📘 الفصل الأول (مجاني)", callback_data='chapter1')],
            [InlineKeyboardButton("🔒 الفصل الثاني", callback_data='chapter2')],
            [InlineKeyboardButton("🔒 الفصل الثالث", callback_data='chapter3')],
            [InlineKeyboardButton("🔒 الفصل الرابع", callback_data='chapter4')],
            [InlineKeyboardButton("🔒 الفصل الخامس", callback_data='chapter5')],
            [InlineKeyboardButton("🔒 الفصل السادس", callback_data='chapter6')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "اهلا بك في منصة الكيمياء السادس العلمي\nاختر الفصل الذي تريد:", 
            reply_markup=reply_markup
        )
        return

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

    # عرض محتوى الدروس مع أزرار العودة
    elif query.data.startswith("lesson"):
        lesson = LESSONS_CHAPTER1.get(query.data)
        if lesson:
            content = f"📖 {lesson['title']}\n\n{lesson['content']}"
            # تقسيم المحتوى إذا كان كبير
            if len(content) > 4000:
                chunks = [content[i:i+4000] for i in range(0, len(content), 4000)]
                for chunk in chunks:
                    await query.message.reply_text(chunk)
            else:
                # أزرار العودة
                keyboard = [
                    [InlineKeyboardButton("↩ العودة لقائمة الدروس", callback_data='chapter1')],
                    [InlineKeyboardButton("🏠 العودة للفصول", callback_data='start_menu')]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.edit_message_text(content, reply_markup=reply_markup)

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
