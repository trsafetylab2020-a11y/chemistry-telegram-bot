import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

# قراءة التوكن من Secrets
TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

# دالة start تعرض رسالة ترحيبية مع أزرار الفصول الستة
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

# دالة لمعالجة الضغط على أزرار الفصول
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'chapter1':
        await query.edit_message_text("📘 الفصل الأول: شرح كامل وملخص ومسائل محلولة")
    else:
        await query.edit_message_text("🔒 هذا الفصل مقفل حالياً، سيصبح متاحاً بعد الاشتراك.")

# إنشاء البوت
app = ApplicationBuilder().token(TOKEN).build()

# إضافة الهاندلر للأوامر والأزرار
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

app.run_polling()
