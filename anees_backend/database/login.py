from bson.objectid import ObjectId

from database.config import users_coll

from models.login import user_login_helper

from security.security import get_password_hash

async def add_user_data_db(data: dict) -> dict:
    data['password'] = get_password_hash(data['password'])
    user = await users_coll.insert_one(data)
    new_user = await users_coll.find_one({"_id":user.inserted_id})
    return user_login_helper(new_user)

async def retrieve_user_data_with_email_id(email_id: str):
    user = await users_coll.find_one({'email_id': email_id})
    if user:
        return user_login_helper(user)
    return None

async def update_user_password_db(id: str, user_type: str, data: dict):
    data["password"] = get_password_hash(data["password"])
    user_data = await users_coll.find_one({"_id": ObjectId(id)})
    if user_data:
        updated_user_data = await users_coll.update_one(
            {"_id": ObjectId(id), "user_type": user_type}, {"$set": data}
        )
        if updated_user_data:
            return True
        return None
    return False