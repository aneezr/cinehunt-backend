import motor.motor_asyncio

# MONGO_DETAILS = "mongodb+srv://idly:idly@cluster0.62ehe.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
MONGO_DETAILS = "mongodb://localhost:27017"

# client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS, tls=True, tlsAllowInvalidCertificates=True)
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)


database = client.Movie_Anees

movie_coll = database.get_collection("Movies collection")
users_coll = database.get_collection("Users collection")

# users_coll.create_index([("name","text")])


# comment the below code after the first run.
# eagle_user_coll.create_index([("country","text"), ("phone_no","text"), ("name","text")])
# user_products_coll.create_index([("title","text"),("details","text")])
# user_services_coll.create_index([("title","text"),("details","text")])
# events_coll.create_index([("title","text"),("description","text")])