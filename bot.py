import _token

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot(_token.api_key, parse_mode=None)


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.send_message(
        message.chat.id, "Seleziona il tipo di carburante:", reply_markup=gen_markup()
    )


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    carburante = call.data
    bot.edit_message_text(
        "Inviami la tua posizione...", call.message.chat.id, call.message.message_id
    )

    """
    if call.data == "benzina":
        bot.answer_callback_query(call.id, "Answer is Benzina")
    elif call.data == "gasolio":
        bot.answer_callback_query(call.id, "Answer is No")
    """


@bot.message_handler(content_types=["location", "venue"])
def handle_location(message):
    location = [message.location.latitude, message.location.longitude]
    print(location)


def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("Benzina", callback_data="benzina"),
        InlineKeyboardButton("Gasolio", callback_data="gasolio"),
    )
    markup.add(
        InlineKeyboardButton("GPL", callback_data="gpl"),
    )
    return markup


bot.infinity_polling()
