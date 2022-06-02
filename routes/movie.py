from typing import List
from fastapi import APIRouter, Body, Depends, status, UploadFile, File, WebSocket, WebSocketDisconnect
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Form

import pandas as pd 

from database.movie import (
    add_movie_data_db,
    get_movie_data_using_id_db,
    get_movie_data_using_movie_title_db
)

from models.movie import (
    Moviegeneration,
    CF,
    movie_ids
)

from functions.func import (
    genre_recommendations,
    CF_func
)

router = APIRouter()

@router.get('get/movie_name/{movie_id}', status_code=status.HTTP_200_OK)
async def get_movie_id_with_movie_name(movie_id: str):
    movie_data = await get_movie_data_using_id_db(id=movie_id)
    if movie_data:
        return movie_data
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Movie data not found')

@router.post('get/movie_id/', status_code=status.HTTP_200_OK)
async def get_movie_name_with_movie_id(mov_data: movie_ids = Body(...)):
    resp = []
    for movie_name in mov_data.movie_names:
        movie_data = await get_movie_data_using_movie_title_db(movie_name)
        resp.append(movie_data)
    return resp
    # for movie_name in movie_names:
    #     print(movie_name)
    #     movie_data = await get_movie_data_using_movie_title_db(movie_name)
    #     print(movie_data)
    #     if movie_data:
    #         resp.append(movie_data)
    # return resp

@router.post('get/recomendation/', status_code=status.HTTP_200_OK)
async def content_based_recomendation(rec_data: Moviegeneration = Body(...)):
    resp_data = genre_recommendations(rec_data.title, rec_data.count)
    return {
        'movie_name': resp_data
    }

@router.post('get/CF/', status_code=status.HTTP_200_OK)
async def get_CF(cf_data: CF = Body(...)):
    resp = []
    resp_data = CF_func(cf_data.usermovieids, cf_data.usermovierates, cf_data.num)
    for key in resp_data.keys():
        movie_data = await get_movie_data_using_id_db(key)
        movie_data['similarity'] = resp_data[key]
        resp.append(movie_data['title'])
    return resp

@router.get('add/movies')
async def add_movies_into_database():
    filename ="static\movies.csv"
    data = pd.read_csv(filename) 
    data_dict = data.to_dict('records')
    # print(data_dict[0])
    for movie in data_dict:
        new_movie = await add_movie_data_db(data=movie)