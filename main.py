from telegram import *
from telegram.ext import *

import config
import database
import lessons
import chapter_tests
import ministerial_questions
import study_plan
import teacher_ai

current_test = {}

async def start(update, context):

    database.add_user(update.effective_user.id)

    keyboard = [

        [InlineKeyboardButton("📘 الفصل الاول (مجاني)", callback_data="ch1")],
        [InlineKeyboardButton("📘 الفصل الثاني", callback_data="ch2")],
        [InlineKeyboardButton("📘 الفصل الثالث", callback_data="ch3")],
        [InlineKeyboardButton("📘 الفصل الرابع", callback_data="ch4")],
        [InlineKeyboardButton("📘 الفصل الخامس", callback_data="ch5")],
        [InlineKeyboardButton("📘 الفصل السادس", callback_data="ch6")],

        [InlineKeyboardButton("🧠 اختبار وزاري", callback_data="wazari")],
        [InlineKeyboardButton("📅 خطة مراجعة 30 يوم", callback_data="plan")],
        [InlineKeyboardButton("❓ اسأل المدرس", callback_data="ask")]

    ]

    await update.message.reply_text(
        "مرحباً بك في بوت كيمياء السادس العلمي",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def chapter(update, context):

    query = update.callback_query
    await query.answer()

    ch = int(query.data[2])

    if ch != 1 and not database.is_paid(query.from_user.id):

        await query.edit_message_text(
            f"هذا الفصل يحتاج اشتراك\nالسعر {config.PRICE} دينار"
        )
        return

    text = lessons.CHAPTERS[ch]

    keyboard = [

        [InlineKeyboardButton("🧠 اختبار الفصل", callback_data=f"test{ch}")],
        [InlineKeyboardButton("⬅️ رجوع", callback_data="back")]

    ]

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def start_test(update, context):

    query = update.callback_query
    await query.answer()

    ch = int(query.data[-1])

    questions = chapter_tests.TESTS[ch]

    current_test[query.from_user.id] = {
        "q": questions,
        "i": 0,
        "score": 0
    }

    await send_question(query)

async def send_question(query):

    data = current_test[query.from_user.id]

    if data["i"] >= len(data["q"]):

        score = data["score"]

        await query.edit_message_text(
            f"انتهى الاختبار\nدرجتك {score}/{len(data['q'])}"
        )

        return

    q = data["q"][data["i"]]

    keyboard = []

    for i, opt in enumerate(q["options"]):
        keyboard.append([InlineKeyboardButton(opt, callback_data=f"a{i}")])

    await query.edit_message_text(
        q["q"],
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def answer(update, context):

    query = update.callback_query
    await query.answer()

    user = query.from_user.id

    data = current_test[user]

    q = data["q"][data["i"]]

    ans = int(query.data[1])

    if ans == q["answer"]:
        data["score"] += 1
        text = "✅ إجابة صحيحة"
    else:
        text = "❌ إجابة خاطئة"

    data["i"] += 1

    keyboard = [
        [InlineKeyboardButton("➡️ التالي", callback_data="next")]
    ]

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def next_question(update, context):

    query = update.callback_query
    await query.answer()

    await send_question(query)

async def plan(update, context):

    query = update.callback_query
    await query.answer()

    text = "\n".join(study_plan.PLAN)

    await query.edit_message_text(text)

async def ask_teacher(update, context):

    text = teacher_ai.answer(update.message.text)

    await update.message.reply_text(text)

app = ApplicationBuilder().token(config.TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(chapter, pattern="ch"))
app.add_handler(CallbackQueryHandler(start_test, pattern="test"))
app.add_handler(CallbackQueryHandler(answer, pattern="a"))
app.add_handler(CallbackQueryHandler(next_question, pattern="next"))
app.add_handler(CallbackQueryHandler(plan, pattern="plan"))

app.run_polling()
