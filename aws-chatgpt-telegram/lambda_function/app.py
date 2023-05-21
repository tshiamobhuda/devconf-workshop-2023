import os
import json
import traceback

import openai
from loguru import logger
from telegram.ext import (
    Dispatcher,
    MessageHandler,
    Filters,
    CommandHandler,
)
from telegram import ParseMode, Update, Bot

# Telegram token
TO_TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
FROM_TELEGRAM_TOKEN = os.environ["TELEGRAM_SECRET_TOKEN"]

# Open API Token
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

# Telegram bot
bot = Bot(token=TO_TELEGRAM_TOKEN)
dispatcher = Dispatcher(bot, None, use_context=True)


# Authenticate Telegram secret token - X-Telegram-Bot-Api-Secret-Token
def authenticate_secret_token(secret_token):
    print(secret_token)
    if secret_token == FROM_TELEGRAM_TOKEN:
        return True
    else:
        return False


#####################
# Telegram Handlers #
#####################


def ask_chatgpt(text):
    message = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "assistant",
                "content": text,
            },
        ],
    )
    logger.info(message)
    return message["choices"][0]["message"]["content"]


def process_voice_message(update, context):
    chat_id = update.message.chat_id
    context.bot.send_message(
        chat_id=chat_id,
        text="Voice Messages are currently not supported.",
        parse_mode=ParseMode.MARKDOWN,
    )


def process_message(update, context):
    chat_id = update.message.chat_id
    chat_text = update.message.text

    try:
        message = ask_chatgpt(chat_text)
    except Exception as e:
        logger.error(e)
        logger.error(traceback.format_exc())
        context.bot.send_message(
            chat_id=chat_id,
            text="There was an exception handling your message.",
            parse_mode=ParseMode.MARKDOWN,
        )
    else:
        print("test")
        # context.bot.send_message(
        #     chat_id=chat_id,
        #     text=message,
        #     parse_mode=ParseMode.MARKDOWN,
        # )


############################
# Lambda Handler functions #
############################

def message_handler(event, context):
    if authenticate_secret_token(json.loads(event["headers"]["X-Telegram-Bot-Api-Secret-Token"])):
        dispatcher.add_handler(MessageHandler(Filters.text, process_message))
        dispatcher.add_handler(MessageHandler(Filters.voice, process_voice_message))

        try:
            update = Update.de_json(json.loads(event["body"]), bot)
            dispatcher.process_update(update)
        except Exception as e:
            logger.error(e)
            return {"statusCode": 500}

        return {"statusCode": 200}
    else:
        return {"statusCode": 403}
