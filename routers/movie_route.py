from typing import Optional, List
from fastapi import APIRouter, Body, HTTPException, Path, Query, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from config.database import Session
from models.movie_model import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie_service import MovieService
from schemas.movie_schema import Movie

movie_router = APIRouter()



@movie_router.get(
    path="/movies",
    tags=["movies"],
    response_model=List[Movie],
    status_code=200,
    # dependencies=[Depends(JWTBearer())],
)
def get_movies() -> List[Movie]:
    db = Session()
    data = MovieService(db).get_movies()
    if not data:
        raise HTTPException(status_code=404, detail='Not Data')
    return jsonable_encoder(data)


@movie_router.get(path="/movies/{id}", tags=["movies"], response_model=Movie, status_code=200)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    data = MovieService(db).get_movie(id)
    if not data:
        raise HTTPException(status_code=404, detail="not found")
    else:
        return JSONResponse(status_code=200, content=jsonable_encoder(data))


@movie_router.get(path="/movies/", tags=["movies"], response_model=List[Movie], status_code=200)
def get_movies_by_category(
    category: str = Query(min_length=5, max_length=15)
) -> List[Movie]:
    db = Session()
    data = MovieService(db).get_movies_by_category(category)
    if not data:
        raise HTTPException(status_code=404, detail="not found")
    else:
        return JSONResponse(status_code=200, content=jsonable_encoder(data))


@movie_router.post(path="/movies", tags=["movies"], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    MovieService(db).create_movie(movie)
    return {"msg": "Se a creado la pelicula"}


@movie_router.put("/movies/{id}", tags=["movies"], response_model=dict, status_code=200)
async def update_movie(id: int, movie: Movie) -> dict:
    db = Session()
    data = MovieService(db).get_movie(id)
    if not data:
        raise HTTPException(status_code=404, detail='Not Found')
    MovieService(db).update_movie(id, movie)
    # for index, item in enumerate(data):
    #     if item["id"] == id:
    #         movies[index].update(movie)
    #         movies[index]["id"] = id
    #         return {"msg": "Se a modificado la pelicula"}
    return {"msg": "Se a modificado la pelicula"}

@movie_router.delete(path="/movies/{id}", tags=["movies"], response_model=dict, status_code=200)
def delete_movie(id: int) -> dict:
    db = Session()
    data = MovieService(db).get_movie(id)
    if not data:
        raise HTTPException(status_code=404, detail='Not Found')
    MovieService(db).delete_movie(id)

    return {"msg": "Se a eliminado la pelicula"}
