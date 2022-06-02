from bson.objectid import ObjectId
from database.config import movie_coll

from models.movie import movie_helper

async def add_movie_data_db(data: dict) -> dict:
    new_data = {
        '_id': data['movieId'],
        'title': data['title'],
        'genres': data['genres']
    }
    user = await movie_coll.insert_one(new_data)
    new_movie = await movie_coll.find_one({"_id":user.inserted_id})
    return movie_helper(new_movie)

async def get_movie_data_using_id_db(id: str) -> dict:
    movie_data = await movie_coll.find_one({"_id": int(id)})
    if movie_data:
        return movie_helper(movie_data)
    return False

async def get_movie_data_using_movie_title_db(title: str) -> dict:
    movie_data = await movie_coll.find_one({"title": title})
    if movie_data:
        return movie_helper(movie_data)
    return False