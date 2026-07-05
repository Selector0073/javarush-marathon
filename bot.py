from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler
from gpt import *
from util import *
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("TELEGRAM-API-KEY")

# *ПОВНИЙ КОД МОЖНА ПЕРЕГЛЯНУТИ НА GITHUB: https://github.com/Selector0073/javarush-marathon

# ---

async def start(update, context):
    #await send_photo(update, context, "avatar_main")
    #await send_text(update, context, "Привіт користувач!")
    msg = load_message("main")
    await send_text(update, context, msg)

async def hello(update, context):
    await send_text_buttons(update, context, "Hello " + update.message.text, {
        "start": "START",
        "stop": "STOP"
    })

async def buttons_handler(update, context):
    query = update.callback_query.data
    if query == "start":
        await send_text(update, context, "You pressed START")
    elif query == "stop":
        await send_text(update, context, "You pressed STOP")

async def gpt(update, context):
    pass

# ---



app = ApplicationBuilder().token(api_key).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))
app.add_handler(CallbackQueryHandler(buttons_handler))

print("Started")

app.run_polling()