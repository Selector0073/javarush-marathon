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

# ---


dialog = Dialog()
dialog.mode = None

chatgpt = ChatGptService(token=openai_api_key)

app = ApplicationBuilder().token(telegram_api_key).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("gpt", gpt))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))

print("Started")

app.run_polling()