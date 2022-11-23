import _token
import getData

from telebot.async_telebot import AsyncTeleBot
import asyncio

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime

bot = AsyncTeleBot(_token.api_key, parse_mode=None)

raggio = 2
carburante = ""


@bot.message_handler(commands=["start"])
async def send_welcome(message):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print(dt_string + " --> Start request from id: " + message.from_user.username)
    await bot.send_message(
        message.chat.id, "Seleziona il tipo di carburante:", reply_markup=gen_markup()
    )


@bot.message_handler(commands=["config"])
async def send_welcome(message):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    await print(
        dt_string + " --> Config request from id: " + message.from_user.username
    )


@bot.callback_query_handler(func=lambda call: True)
async def callback_query(call):
    global carburante, raggio
    carburante = call.data
    if carburante == "radius":
        await bot.answer_callback_query(callback_query_id=call.id)
        return
    if carburante == "rp":
        if raggio < 1:
            raggio += 0.1
            if raggio == 1:
                raggio = int(raggio)
        else:
            raggio = int(raggio)
            if raggio >= 20:
                await bot.answer_callback_query(callback_query_id=call.id)
                return
            raggio += 1
        await bot.answer_callback_query(callback_query_id=call.id)
        await bot.edit_message_text(
            "Seleziona il tipo di carburante: ",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=gen_markup(),
        )
        return
    if carburante == "rm":
        if raggio <= 1:
            if raggio <= 0.15:
                await bot.answer_callback_query(callback_query_id=call.id)
                return
            raggio -= 0.1
        else:
            raggio -= 1
        await bot.answer_callback_query(callback_query_id=call.id)
        await bot.edit_message_text(
            "Seleziona il tipo di carburante: ",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=gen_markup(),
        )
        return
    await bot.edit_message_text(
        "Inviami la tua posizione...", call.message.chat.id, call.message.message_id
    )


@bot.message_handler(content_types=["location", "venue"])
async def handle_location(message):
    global carburante
    if carburante not in ("1-1", "2-1", "4-x"):
        await bot.send_message(
            message.chat.id,
            "\U000026A0 Seleziona prima il tipo di carburante:",
            reply_markup=gen_markup(),
        )
        return
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print(
        dt_string
        + " --> Request prezzi from id: "
        + message.from_user.username
        + " carburante: "
        + carburante
    )
    location = [message.location.latitude, message.location.longitude]
    prezzi = getData.cerca_prezzo(
        location, carburante, raggio
    )  # 5 in questo caso è la distanza
    if prezzi == -1:
        await bot.send_message(
            message.chat.id,
            "Nessun benzinaio trovato nell'area selezionata\nriprova con un raggio maggiore",
        )
        await bot.send_message(
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

    await bot.send_message(message.chat.id, msg_buf, parse_mode="HTML")


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


asyncio.run(bot.polling(non_stop=True, request_timeout=90))
