from pydantic_core.core_schema import none_schema
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler

from gpt import *
from util import *

async def start(update, context):
    dialog.mode = "main"
    text = load_message("main")
    await  send_photo(update, context, "main")
    await  send_text(update, context, text)

    await show_main_menu(update, context,{
        "start":"Главное меню бота 😘",
        "profile": "Генерация Tinder-профля 😎",
        "opener": "Сообщение для знакомства 🥰",
        "message": "Переписка от вашего имени 😈",
        "date": "переписка со звездами 🔥",
        "gpt":"Задать вопрос чату GPT 🧠"
    })


async def gpt(update, context):
    dialog.mode = "gpt"
    text = load_message("gpt")
    await send_photo(update, context, "gpt")
    await send_text(update, context, text)

async def gpt_dialog(update, context):
    text = update.message.text
    prompt = load_prompt("gpt")
    answer = await chatgpt.send_question(prompt, text)
    await send_text(update, context, answer)

async def hello(update, context):
    if dialog.mode == "gpt":
        await gpt_dialog(update, context)
    else:
        await  send_text(update, context, "*Привет*")
        await  send_text(update, context, "_Как дела?_")
        await  send_text(update, context, "Вы написали: " + update.message.text)
        await  send_photo(update, context, "avatar_main")
        await send_text_buttons(update, context, "Запустить процесс?", {
            "start":"Запустить",
            "stop": "Остановить"
        })

async def hello_button(update, context):
    query = update.callback_query.data
    if query == "start":
        await  send_text(update, context, "*Процесс запущен*")
    else:
        await send_text(update, context, "*Процесс остановлен*")

dialog = Dialog()
dialog.mode = None

chatgpt = ChatGptService(token="gpt:A03NYofv3ubgIx6f1SXnPAKmBZ0E9dS9Qcn2T2Zi1nOgo_QvJ0z8W5cWFvJFkblB3TavDiNT25x1--mRNrTISss9Vj3Q6lCoImv5cXw51H8RE70DG7rsRaf4bEE4")

app = ApplicationBuilder().token("7891141647:AAHgvYl2QM08R4GG6Wv90f5YxREh5H1jrxk").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("gpt", gpt))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))
app.add_handler(CallbackQueryHandler(hello_button))
app.run_polling()
