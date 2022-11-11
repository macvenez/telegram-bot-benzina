import _token
import getData

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot(_token.api_key_development, parse_mode=None)

raggio = 2
carburante = ""


@bot.message_handler(commands=["start"])
def send_welcome(message):
    print("Start request from id: " + message.from_user.username)
    bot.send_message(
        message.chat.id, "Seleziona il tipo di carburante:", reply_markup=gen_markup()
    )


@bot.message_handler(commands=["config"])
def send_welcome(message):
    print("Config request from id: " + message.from_user.username)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global carburante, raggio
    carburante = call.data
    if carburante == "radius":
        bot.answer_callback_query(callback_query_id=call.id)
        return
    if carburante == "rp":
        if raggio < 1:
            raggio += 0.1
            if raggio == 1:
                raggio = int(raggio)
        else:
            raggio = int(raggio)
            if raggio >= 20:
                bot.answer_callback_query(callback_query_id=call.id)
                return
            raggio += 1
        bot.answer_callback_query(callback_query_id=call.id)
        bot.edit_message_text(
            "Seleziona il tipo di carburante: ",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=gen_markup(),
        )
        return
    if carburante == "rm":
        if raggio <= 1:
            if raggio <= 0.15:
                bot.answer_callback_query(callback_query_id=call.id)
                return
            raggio -= 0.1
        else:
            raggio -= 1
        bot.answer_callback_query(callback_query_id=call.id)
        bot.edit_message_text(
            "Seleziona il tipo di carburante: ",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=gen_markup(),
        )
        return
    bot.edit_message_text(
        "Inviami la tua posizione...", call.message.chat.id, call.message.message_id
    )


@bot.message_handler(content_types=["location", "venue"])
def handle_location(message):
    global carburante
    if carburante not in ("1-1", "2-1", "4-x"):
        bot.send_message(
            message.chat.id,
            "\U000026A0 Seleziona prima il tipo di carburante:",
            reply_markup=gen_markup(),
        )
        return
    print(
        "Request prezzi from id: "
        + message.from_user.username
        + " carburante: "
        + carburante
    )
    location = [message.location.latitude, message.location.longitude]
    prezzi = getData.cerca_prezzo(
        location, carburante, raggio
    )  # 5 in questo caso è la distanza
    if prezzi == -1:
        bot.send_message(
            message.chat.id,
            "Nessun benzinaio trovato nell'area selezionata\nriprova con un raggio maggiore",
        )
        bot.send_message(
            message.chat.id,
            "Seleziona il tipo di carburante:",
            reply_markup=gen_markup(),
        )
        return
    max_benzinai = 5
    msg_buf = ""
    for i, item in enumerate(prezzi):
        if i == max_benzinai:
            break
        else:
            if i == 0:
                msg_buf += "\U0001F947"
            if i == 1:
                msg_buf += "\U0001F948"
            if i == 2:
                msg_buf += "\U0001F949"
            if i > 2:
                msg_buf += "  " + str(i + 1) + " "
            msg_buf += "-"
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
                + "€/l "
                + nome
                + "</a>"
                + prezzi[i]["icon"]
                + "\n"
            )

    bot.send_message(message.chat.id, msg_buf, parse_mode="HTML")


def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    markup.add(
        InlineKeyboardButton("-", callback_data="rm"),
        InlineKeyboardButton(
            "Raggio (km): " + str(round(raggio, 1)), callback_data="radius"
        ),
        InlineKeyboardButton("+", callback_data="rp"),
    )
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
