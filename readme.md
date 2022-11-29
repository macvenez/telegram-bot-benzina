<p align="center">
<img align="center" width="100px" src="https://www.venez.it/assets/gas-pump.png" alt="benzina_logo" />
<h1 align="center">Telegram Bot Benzina</h1>
</p>


 You can find this bot at:
[@prezzi_benzina_bot](https://t.me/prezzi_benzina_bot)


# Introduction
This project was born during the high fuel price rising in 2022. It was suggested by a friend of mine and I wanted to test myself into something really useful.  

DISCLAIMER: As I'm not very sure about legal issues with using API to get fuel prices I decided to hide the url and headers content. BTW the API is public so it should technically be allowed to "scrape" the public data, at least for personal use.  

The data I'm using are from Italian public [OsservaPrezzi Carburanti website](https://carburanti.mise.gov.it/ospzSearch/home). This service is bound to the actual REAL fuel prices in Italy (as fuel pump owners are required to share current gas prices), so it's not using any community shared gas prices and data should always be up to date with the current gas prices

# Installation and prerequisites
Simply get this repo by 
```
git clone https://github.com/macvenez/telegram-bot-benzina.git
```
```
cd telegram-bot-benzina
```
Then you should create your personal _secret.py file that should just contain the following:
```
api_key=<Your telegram bot api-key>
```
You can get this from the BotFather Telegram's bot.  
You can also just hardcode your apikey instead of including it externally
## Dependencies
In order to use the bot you should have the following python packages:
- [pyTelegramBot](https://github.com/eternnoir/pyTelegramBotAPI)
- [geopy](https://github.com/geopy/geopy)
- [aiohttp](https://github.com/aio-libs/aiohttp)  

You can get all these packages by (assuming you have python-pip):
```
pip install pyTelegramBotAPI aiohttp geopy
```

# Running the bot
Now you can just run the bot with
```
python bot.py

```

# Commands and usage
Actually there's only a command
* `/start`: Start the bot and choose fuel type and distance  
After selecting that you'll be asked to send your position, you can do that by using the "attach icon" :paperclip: and selecting Location :pushpin:

# Contributors and references
![GitHub Contributors Image](https://contrib.rocks/image?repo=macvenez/telegram-bot-benzina)  

[Fuel icons created by Freepik - Flaticon](https://www.flaticon.com/free-icons/fuel)