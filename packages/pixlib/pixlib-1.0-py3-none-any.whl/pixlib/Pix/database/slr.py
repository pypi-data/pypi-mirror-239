from pixlib.Pix.database import db_x

db = db_x

collection = db['slr']
async def pix_user(chat):
    doc = {"_id": "slr", "users": [chat]}
    r = await collection.find_one({"_id": "slr"})
    if r:
        await collection.update_one({"_id": "slr"}, {"$push": {"users": chat}})
    else:
        await collection.insert_one(doc)


async def get_pix_users():
    results = await collection.find_one({"_id": "slr"})
    if results:
        return results["users"]
    else:
        return []


async def unpix_user(chat):
    await collection.update_one({"_id": "slr"}, {"$pull": {"users": chat}})