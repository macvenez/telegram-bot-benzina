import _secret
import getData, dbLink

from telebot.async_telebot import AsyncTeleBot
import asyncio

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime

bot = AsyncTeleBot(_secret.api_key_development, parse_mode=None)

default_radius = 2
default_max_displayed = 5

currUsers = {}


@bot.message_handler(commands=["start"])
async def send_welcome(message):
    global max_displayed, radius, currUsers
    user_id = message.from_user.id
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print(dt_string + " --> Start request from id: " + str(user_id))

    if user_id not in currUsers:
        dbData = dbLink.getData(user_id)
        if dbData == 0:
            dbLink.addUser(
                user_id, default_max_displayed, default_radius
            )  # create a new user with default settings
        else:
            currUsers[user_id] = {
                "max_displayed": int(dbData[0]),
                "radius": float(dbData[1]),
                "options": "",
            }  # get data saved in database
    await bot.send_message(
        message.chat.id,
        "Seleziona il tipo di carburante:",
        reply_markup=gen_markup(user_id),
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
    user_id = call.message.chat.id
    global currUsers
    currUsers[user_id]["options"] = call.data
    if (
        currUsers[user_id]["options"] == "radius"
        or currUsers[user_id]["options"] == "displayed"
    ):
        await bot.answer_callback_query(callback_query_id=call.id)
        return
    if currUsers[user_id]["options"] == "rp":
        if currUsers[user_id]["radius"] < 1:
            currUsers[user_id]["radius"] += 0.1
            if currUsers[user_id]["radius"] == 1:
                currUsers[user_id]["radius"] = int(currUsers[user_id]["radius"])
        else:
            currUsers[user_id]["radius"] = int(currUsers[user_id]["radius"])
            if currUsers[user_id]["radius"] >= 20:
                await bot.answer_callback_query(callback_query_id=call.id)
                return
            currUsers[user_id]["radius"] += 1
        await bot.answer_callback_query(callback_query_id=call.id)
        await bot.edit_message_text(
            "Seleziona il tipo di carburante: ",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=gen_markup(user_id),
        )
        return
    if currUsers[user_id]["options"] == "rm":
        if currUsers[user_id]["radius"] <= 1:
            if currUsers[user_id]["radius"] <= 0.15:
                await bot.answer_callback_query(callback_query_id=call.id)
                return
            currUsers[user_id]["radius"] -= 0.1
        else:
            currUsers[user_id]["radius"] -= 1
        await bot.answer_callback_query(callback_query_id=call.id)
        await bot.edit_message_text(
            "Seleziona il tipo di carburante: ",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=gen_markup(user_id),
        )
        return
    if currUsers[user_id]["options"] == "dp":
        if currUsers[user_id]["max_displayed"] >= 10:
            await bot.answer_callback_query(callback_query_id=call.id)
            return
        else:
            currUsers[user_id]["max_displayed"] += 1
            await bot.answer_callback_query(callback_query_id=call.id)
            await bot.edit_message_text(
                "Seleziona il tipo di carburante: ",
                call.message.chat.id,
                call.message.message_id,
                reply_markup=gen_markup(user_id),
            )
            return
    if currUsers[user_id]["options"] == "dm":
        if currUsers[user_id]["max_displayed"] == 1:
            await bot.answer_callback_query(callback_query_id=call.id)
            return
        else:
            currUsers[user_id]["max_displayed"] -= 1
            await bot.answer_callback_query(callback_query_id=call.id)
            await bot.edit_message_text(
                "Seleziona il tipo di carburante: ",
                call.message.chat.id,
                call.message.message_id,
                reply_markup=gen_markup(user_id),
            )
            return

    await bot.edit_message_text(
        "Inviami la tua posizione...", call.message.chat.id, call.message.message_id
    )


@bot.message_handler(content_types=["location", "venue"])
async def handle_location(message):
    user_id = message.from_user.id
    global currUsers
    if user_id not in currUsers:
        dbData = dbLink.getData(user_id)
        if dbData == 0:
            dbLink.addUser(
                user_id, default_max_displayed, default_radius
            )  # create a new user with default settings
        else:
            currUsers[user_id] = {
                "max_displayed": int(dbData[0]),
                "radius": float(dbData[1]),
                "options": "",
            }  # get data saved in database
        await bot.send_message(
            message.chat.id,
            "\U000026A0 Seleziona prima il tipo di carburante:",
            reply_markup=gen_markup(user_id),
        )
        return
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print(
        dt_string
        + " --> Request prezzi from id: "
        + str(user_id)
        + " carburante: "
        + str(currUsers[user_id]["options"])
    )
    location = [message.location.latitude, message.location.longitude]
    prezzi = getData.cerca_prezzo(
        location, currUsers[user_id]["options"], currUsers[user_id]["radius"]
    )
    if prezzi == -1:
        await bot.send_message(
            message.chat.id,
            "Nessun benzinaio trovato nell'area selezionata\nriprova con un raggio maggiore",
        )
        await bot.send_message(
            message.chat.id,
            "Seleziona il tipo di carburante:",
            reply_markup=gen_markup(user_id),
        )
        return
    msg_buf = ""
    for i, item in enumerate(prezzi):
        if i == currUsers[user_id]["max_displayed"]:
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
                + "</a> ("
                + str(round(prezzi[i]["dist"], 1))
                + "km)\n"
            )

    await bot.send_message(message.chat.id, msg_buf, parse_mode="HTML")
    dbLink.performRequest(user_id)
    dbLink.updateData(
        user_id, currUsers[user_id]["max_displayed"], currUsers[user_id]["radius"]
    )
    del currUsers[user_id]


def gen_markup(user_id):
    global currUsers
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    markup.add(
        InlineKeyboardButton("-", callback_data="rm"),
        InlineKeyboardButton(
            "Raggio (km): " + str(round(currUsers[user_id]["radius"], 1)),
            callback_data="radius",
        ),
        InlineKeyboardButton("+", callback_data="rp"),
    )
    markup.add(
        InlineKeyboardButton("-", callback_data="dm"),
        InlineKeyboardButton(
            "Distributori: " + str(currUsers[user_id]["max_displayed"]),
            callback_data="displayed",
        ),
        InlineKeyboardButton("+", callback_data="dp"),
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


dbLink.initDB()
asyncio.run(bot.polling(non_stop=True, request_timeout=90))
