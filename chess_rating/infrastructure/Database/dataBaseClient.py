from sqlalchemy import engine
from sqlalchemy import create_engine, text
from typing import Dict, List, Tuple
from chess_rating.infrastructure.Database.profile import Profile



class DatabaseClient: 
    _instance = None

    def __new__(cls, *args, **kwargs): 
        if cls._instance == None:
            cls._instance = super().__new__(cls)
            cls._instance.initalized = False  # czy juz bylo
        return cls._instance


    def __init__(self, DB_URL: str):
        if self.initalized:
            return

        self.db_url: str = DB_URL
        self.engine = create_engine(self.db_url, connect_args={"connect_timeout": 30})
        self.initalized = True

    def _insertData(self):
        return text(
                    "INSERT INTO users (nazwa, rating) "
                    "VALUES (:nazwa, :rating) "
                    "ON CONFLICT (nazwa) "
                    "DO UPDATE SET rating = EXCLUDED.rating"
                )
    def _deleteUser(self):        
        return text("DELETE FROM users WHERE nazwa = :proper_username")

    def _get_users(self):
        return text(
                    "SELECT * FROM users"
                )
            


    def insertData(self, profil: Profile) -> None:
        conn = self.engine.connect()
        try:
            conn.execute(self._insertData(),profil.to_dict())
        finally:
            conn.commit() 
            conn.close()


    def get_users(self) -> List[Profile]:
        conn = self.engine.connect()
        try: 
            result = conn.execute(self._get_users()).fetchall()
            profiles_list: List[Profile] = []
            for row in result:
                profiles_list.append(Profile(nazwa = row[0], rating = row[1]))
        finally:
            conn.close()
        return profiles_list

    def delete_user(self,username: str) -> Tuple:
        proper_username = username.lower()
        conn = self.engine.connect()
        try:
            result = conn.execute(self._deleteUser(),
                         {"proper_username": proper_username})
            conn.commit()
        finally:
            conn.close()
        return (result) 