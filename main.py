from pyrogram import Client, enums
plugins = dict(root="bot")

bot = Client("my_bot",
             api_id = str(open('FILES/config.txt',encoding="UTF-8").read().splitlines()[0]) ,
             api_hash = str(open('FILES/config.txt',encoding="UTF-8").read().splitlines()[1]) ,
             bot_token = str(open('FILES/config.txt',encoding="UTF-8").read().splitlines()[2]) ,
             plugins = plugins)
#ALSO REPLACE THE BOT TOKEN IN SCRAPER.PY FILES BRO
bot.set_parse_mode(enums.ParseMode.HTML)

from scraper import *
print("Done Bot Active ✅")
print("NOW START BOT ONCE MY MASTER")

bot.run()