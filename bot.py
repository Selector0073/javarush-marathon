from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler
from gpt import *
from util import *
import os
from dotenv import load_dotenv

load_dotenv()

telegram_api_key = os.getenv("TELEGRAM-API-KEY")
openai_api_key = os.getenv("OPEN-AI-API-KEY")

# *ПОВНИЙ КОД МОЖНА ПЕРЕГЛЯНУТИ НА GITHUB: https://github.com/Selector0073/javarush-marathon

# ---

async def start(update, context):
    msg = load_message("main")
    await send_photo(update, context, "main")
    await send_text(update, context, msg)
    await show_main_menu(update,context, {
        "start": "Головне меню",
        "profile": "Генерація Tinder-профіля \uD83D\uDE0E", 
        "opener": "Повідомлення для знайомства \uD83E\uDD70", 
        "message": "Переписка вiд вашого імені \uD83D\uDE08", 
        "date": "Спілкування з зірками \uD83D\uDD25", 
        "gpt": "Задати питання ChatGPт \uD83E\uDDE0"
    })

async def gpt(update, context):
    dialog.mode = "gpt"
    await send_photo(update, context, "gpt")
    msg = load_message("gpt")
    await send_text(update, context, msg)

async def gpt_dialog(update, context):
    text = update.message.text
    promt = load_prompt("gpt")
    answer = await chatgpt.send_question(promt, text)
    await send_text(update, context, answer)

async def hello(update, context):
    if dialog.mode == "gpt":
        await gpt_dialog(update, context)
    elif dialog.mode == "date":
        await date_dialog(update, context)
    elif dialog.mode == "message":
        await message_dialog(update, context)

async def date_button(update, context):
    query = update.callback_query.data
    await update.callback_query.answer()
    await send_photo(update, context, query)
    await send_text(update, context, "Гарний вибірю \uD83D\uDE05 Ваша задача запросити дівчину/хлопця на побачення за 5 повідомлень.")
    promt = load_prompt(query)
    chatgpt.set_promt(promt)

async def date_dialog(update, context):
    text = update.message.text
    my_message = await send_text(update, context, "Відправляю повідомлення...")
    answer = await chatgpt.add_message(text)
    await my_message.edit_text(answer)

async def message(update, context):
    dialog.mode = "message"
    msg = load_message("message")
    await send_photo(update, context, "message")
    await send_text_buttons(update, context, msg, {
        "message_next": "Написати повідомлення",
        "message_date": "Запростити на побачення",
    })
    dialog.list.clear()

async def message_dialog(update, context):
    text = update.message.text
    dialog.list.append(text)

async def message_button(update, context):
    query = update.callback_query.data
    await update.callback_query.answer()
    prompt = load_prompt(query)
    user_chat_history = "\n\n".join(dialog.list)
    my_message = await send_text(update, context, "Думаю над варіантами...")
    answer = await chatgpt.send_question(prompt, user_chat_history)
    await my_message.edit_text(answer)

async def date(update, context):
    dialog.mode = "date"
    msg = load_message("date")
    await send_photo(update, context, "date")
    await send_text_buttons(update, context, msg, {
        "date_grande": "Аріана гранде",
        "date_robby": "Марго Роббі",
        "date_zendaya": "Зендея",
        "date_gosling": "Раян Гослінг",
        "date_hardy": "Том Гарді"
    })

# ---


dialog = Dialog()
dialog.mode = None
dialog.list = []

chatgpt = ChatGptService(token=openai_api_key)

app = ApplicationBuilder().token(telegram_api_key).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("gpt", gpt))
app.add_handler(CommandHandler("date", date))
app.add_handler(CommandHandler("message", message))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))
app.add_handler(CallbackQueryHandler(date_button, pattern="^date_.*"))
app.add_handler(CallbackQueryHandler(message_button, pattern="^message_.*"))

print("Started")

app.run_polling()