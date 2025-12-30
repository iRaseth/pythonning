import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from chess_rating.infrastructure.api.client import ApiClient
from chess_rating.infrastructure.Database.dataBaseClient import DatabaseClient
from chess_rating.infrastructure.Database.profile import Profile
from typing import List, Dict
from http import HTTPStatus
from chess_rating.infrastructure.transformer.transform import Transform
from chess_rating.infrastructure.api.User import User

app = FastAPI()

Klient = ApiClient()
KlientBaza = DatabaseClient("postgresql+psycopg2://postgres:Innominate12@172.25.240.1:1234/chess_api")
Transformer = Transform()

Uzytkownik = User(Klient,KlientBaza,Transformer)


origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins =origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]   
)

@app.get("/users", response_model=List[Profile])
def get_users_api():
    return Uzytkownik.get_users()



@app.post("/add_user/{username}", response_model=List[Profile])
def add_one_user(username: str) -> List[Profile]:
    database_data = Uzytkownik.get_users()
    if username in database_data:
        return [{"Nazwa": "user alerady in base"}]
    data = Uzytkownik.get(username)
    if "code" in data.keys():
         raise HTTPException(
            status_code=404,
            detail="Nie udało się znaleźć użytkownika"
        )
    transformed_data = Uzytkownik.transform_data_to_profile(data)
    Uzytkownik.insertData(transformed_data)
        
    return [transformed_data]

@app.delete("/delete_user/{username}")
def delete_user(username: str) -> None:
    Uzytkownik.delete_user(username)




