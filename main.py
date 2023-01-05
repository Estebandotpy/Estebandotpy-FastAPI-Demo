from fastapi import FastAPI
from pydantic import BaseModel
from utils.jwt_manager import create_token
from routers.user_route import auth_routers
from routers.movie_route import movie_router
from config.database import engine, Base
from middlewares.handler_error import HandlerError
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI()
app.title = "Movie API"
app.version = "0.0.1"

app.add_middleware(HandlerError)
app.include_router(movie_router)
app.include_router(auth_routers)

Base.metadata.create_all(bind=engine)

@app.get(path="/", tags=["Home"])
def message():
    return HTMLResponse("<h1>Hi from FastAPI</h1>")


