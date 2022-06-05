from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.movie import router as MovieRouter
from routes.login import router as LoginRouter

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://online-movie-database.p.rapidapi.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(LoginRouter, tags=["Login"], prefix="")
app.include_router(MovieRouter, tags=["Movies"], prefix="/movie")