import pymongo
import json

mongo_uri = MONGO_URI
mongo_db = "remotasks"
client = pymongo.MongoClient(MONGO_URI)
db = client[mongo_db]

text = open("mrporter.json", "r")
data = json.loads(text.read())
text.close()
counter = 0
for d in data[28700:]:
    # find = db["mrpotrer"].find_one({"SKU": d["SKU"], "product_id": d["product_id"]})
    # if not find:
    try:

        db["mrpotrer"].insert_one(d)
    except:
        pass
    print(counter)
    counter += 1