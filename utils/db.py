from pymongo.mongo_client import MongoClient
from datetime import date

uri = "MONGO_DB_URL"
mongo = MongoClient(uri).Rankings
chatdb = mongo.chat


def increase_count(chat, user):
    user = str(user)
    today = str(date.today())
    user_db = chatdb.find_one({"chat": chat})

    if not user_db:
        user_db = {}
    elif not user_db.get(today):
        user_db = {}
    else:
        user_db = user_db[today]

    if user in user_db:
        user_db[user] += 1
    else:
        user_db[user] = 1

    #  print(user_db)
    chatdb.update_one({"chat": chat}, {"$set": {today: user_db}}, upsert=True)


name_cache = {}


async def get_name(app, id):
    global name_cache

    if id in name_cache:
        return name_cache[id]
    else:
        try:
            i = await app.get_users(id)
            i = f'{(i.first_name or "")} {(i.last_name or "")}'
            name_cache[id] = i
            return i
        except:
            return id
