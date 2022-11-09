import _token
import getData

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot(_token.api_key, parse_mode=None)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    print("Start request from id: " + message.from_user.username)
    bot.send_message(
        message.chat.id, "Seleziona il tipo di carburante:", reply_markup=gen_markup()
    )


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global carburante
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
    print(
        "Request prezzi from id: "
        + message.from_user.username
        + " carburante: "
        + carburante
    )
    location = [message.location.latitude, message.location.longitude]
    prezzi = getData.cerca_prezzo(location, carburante, 5)
    max_benzinai = 5
    msg_buf = ""
    for i, item in enumerate(prezzi):
        if i == max_benzinai:
            break
        else:
            if i == 0:
                msg_buf += "\U0001F947 "
            if i == 1:
                msg_buf += "\U0001F948 "
            if i == 2:
                msg_buf += "\U0001F949 "
            if i > 2:
                msg_buf += str(i + 1)
            msg_buf += " - "
            location_buf = (
                str(prezzi[i]["coord"]["lat"]) + "," + str(prezzi[i]["coord"]["lng"])
            )
            nome = prezzi[i]["marca"]
            if nome == "PompeBianche":
                nome = prezzi[i]["nome"]
            msg_buf += (
                '<a href="https://maps.google.com/?q='
                + location_buf
                + '">'
                + str(prezzi[i]["prezzo"])
                + "€/l - "
                + nome
                + "</a>\n"
            )

    bot.send_message(message.chat.id, msg_buf, parse_mode="HTML")


def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("Benzina", callback_data="1-1"),
        InlineKeyboardButton("Gasolio", callback_data="2-1"),
    )
    markup.add(
        InlineKeyboardButton("GPL", callback_data="4-x"),
    )
    return markup


bot.infinity_polling()
