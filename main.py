import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

ADMIN_ID = 671598385
KI_CARD = "5556960115150247"

scores = {}
current_question = {}

# الدروس
LESSONS = {

"atom":{
"title":"تركيب الذرة",
"text":"""
⚛️ تركيب الذرة

الذرة أصغر جزء من العنصر يحتفظ بخواصه الكيميائية.

تتكون الذرة من:
• بروتونات موجبة
• نيوترونات متعادلة
• إلكترونات سالبة

العدد الذري = عدد البروتونات

العدد الكتلي = عدد البروتونات + عدد النيوترونات
""",
"video":"https://www.youtube.com/watch?v=Nh9yq3cOVsY"
},

"periodic":{
"title":"الجدول الدوري",
"text":"""
📊 الجدول الدوري

ترتب العناصر في الجدول الدوري حسب العدد الذري تصاعدياً.

يتكون الجدول الدوري من:

• دورات أفقية
• مجاميع عمودية

العناصر في نفس المجموعة تتشابه في الخواص الكيميائية.
""",
"video":"https://www.youtube.com/watch?v=0RRVV4Diomg"
}

}

# الاسئلة
QUESTIONS = [

{
"q":"ما المقصود بالعدد الذري؟",
"options":[
"عدد البروتونات",
"عدد النيوترونات",
"عدد الالكترونات",
"العدد الكتلي"
],
"answer":0
},

{
"q":"ما العدد الكتلي؟",
"options":[
"عدد البروتونات",
"عدد البروتونات + النيوترونات",
"عدد الالكترونات",
"عدد المدارات"
],
"answer":1
}

]

# start
async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):

    keyboard=[

[InlineKeyboardButton("📘 الفصل الأول",callback_data="chapter1")],
[InlineKeyboardButton("📚 الملازم",callback_data="pdf")],
[InlineKeyboardButton("🧠 الاختبار",callback_data="test")],
[InlineKeyboardButton("📊 درجاتي",callback_data="score")],
[InlineKeyboardButton("💳 الاشتراك",callback_data="sub")]

]

    await update.message.reply_text(
"📚 منصة كيمياء السادس العلمي",
reply_markup=InlineKeyboardMarkup(keyboard)
)

# الازرار
async def buttons(update:Update,context:ContextTypes.DEFAULT_TYPE):

    query=update.callback_query
    user=query.from_user.id

    await query.answer()

# الفصل الاول
    if query.data=="chapter1":

        keyboard=[

[InlineKeyboardButton("⚛️ تركيب الذرة",callback_data="lesson_atom")],
[InlineKeyboardButton("📊 الجدول الدوري",callback_data="lesson_periodic")],
[InlineKeyboardButton("🧠 اختبار الفصل",callback_data="test")],
[InlineKeyboardButton("⬅️ رجوع",callback_data="back")]

]

        await query.edit_message_text(
"📘 الفصل الأول",
reply_markup=InlineKeyboardMarkup(keyboard)
)

# عرض الدرس
    elif query.data.startswith("lesson_"):

        lesson=query.data.replace("lesson_","")

        data=LESSONS[lesson]

        keyboard=[

[InlineKeyboardButton("🎥 فيديو الشرح",url=data["video"])],
[InlineKeyboardButton("🧠 اختبار",callback_data="test")],
[InlineKeyboardButton("⬅️ رجوع",callback_data="chapter1")]

]

        await query.edit_message_text(
data["text"],
reply_markup=InlineKeyboardMarkup(keyboard)
)

# الاختبار
    elif query.data=="test":

        q=random.choice(QUESTIONS)

        current_question[user]=q

        keyboard=[]

        for i,opt in enumerate(q["options"]):

            keyboard.append([InlineKeyboardButton(opt,callback_data=f"ans_{i}")])

        await query.edit_message_text(
q["q"],
reply_markup=InlineKeyboardMarkup(keyboard)
)

# الاجابة
    elif query.data.startswith("ans_"):

        user_answer=int(query.data.split("_")[1])

        q=current_question[user]

        correct=q["answer"]

        if user_answer==correct:

            scores[user]=scores.get(user,0)+1

            text="✅ إجابة صحيحة"

        else:

            text=f"❌ إجابة خاطئة\nالإجابة الصحيحة: {q['options'][correct]}"

        keyboard=[

[InlineKeyboardButton("➡️ السؤال التالي",callback_data="test")],
[InlineKeyboardButton("⬅️ رجوع",callback_data="back")]

]

        await query.edit_message_text(
text,
reply_markup=InlineKeyboardMarkup(keyboard)
)

# الدرجات
    elif query.data=="score":

        s=scores.get(user,0)

        await query.edit_message_text(
f"📊 مجموع درجاتك: {s}"
)

# الملازم
    elif query.data=="pdf":

        keyboard=[

[InlineKeyboardButton("📄 ملزمة الشرح",url="https://drive.google.com/file/d/1vSK6SxkQRQl23aVR4RvZgpuUbHW0iUsT/view")],
[InlineKeyboardButton("📄 ملزمة ثانية",url="https://drive.google.com/file/d/1uxzE2l43iLopD81axegAEY0iFVCeEJmq/view")],
[InlineKeyboardButton("📄 الوزاريات",url="https://drive.google.com/file/d/15Y1Ozad8T3FEuu_Wc3hpR97dxjSTxvbQ/view")],
[InlineKeyboardButton("⬅️ رجوع",callback_data="back")]

]

        await query.edit_message_text(
"📚 مكتبة الملازم",
reply_markup=InlineKeyboardMarkup(keyboard)
)

# الاشتراك
    elif query.data=="sub":

        await query.edit_message_text(
f"""
💳 الاشتراك الكامل لجميع الفصول

السعر: 25000 دينار

الدفع عبر كي كارد:

{KI_CARD}
"""
)

# رجوع
    elif query.data=="back":

        keyboard=[

[InlineKeyboardButton("📘 الفصل الأول",callback_data="chapter1")],
[InlineKeyboardButton("📚 الملازم",callback_data="pdf")],
[InlineKeyboardButton("🧠 الاختبار",callback_data="test")],
[InlineKeyboardButton("📊 درجاتي",callback_data="score")],
[InlineKeyboardButton("💳 الاشتراك",callback_data="sub")]

]

        await query.edit_message_text(
"القائمة الرئيسية",
reply_markup=InlineKeyboardMarkup(keyboard)
)

app=ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start",start))
app.add_handler(CallbackQueryHandler(buttons))

app.run_polling()
