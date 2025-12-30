import pytest
from chess_rating.infrastructure.api.client import ApiClient
from chess_rating.infrastructure.Database.dataBaseClient import DatabaseClient
from chess_rating.infrastructure.Database.profile import Profile
from chess_rating.infrastructure.transformer.transform import Transform
import psycopg2
from unittest.mock import MagicMock

def test_add_to_database() -> None:
    KlientBaza  = DatabaseClient("postgresql+psycopg2://postgres:[haslo]gi@172.25.240.1:1234/chess_api")
    Klient = ApiClient()
    KlientTransform = Transform()
    data = Klient.get("ronaldinhoszahuf")
    transformed = KlientTransform.transform_data_to_profile(data)
 
    data2 = KlientBaza.get_users()

    print(data2)
    
    assert type(transformed) == Profile
    assert {"nazwa": "ronaldinhoszahuf", "rating": 1771} == transformed.to_dict()


   

