import pymongo

client = pymongo.MongoClient(
 "mongodb+srv://robindoch037:ciQ2GQMncZRSlzof@bot.bp7mokd.mongodb.net/?retryWrites=true&w=majority"
)
result = str(client)

if "connect=True" in result:
    print("MONGODB CONNECTED SUCCESSFULLY ✅")
else:
    print("MONGODB CONNECTION FAILED ❌")

folder = client["bot"]
usersdb = folder.USERSDB
chats_auth = folder.CHATS_AUTH
gcdb = folder.GCDB
