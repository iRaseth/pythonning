from sqlalchemy import engine
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import OperationalError

from typing import Dict, List, Tuple
from chess_rating.infrastructure.Database.profile import Profile
from typing import Any, Protocol
from chess_rating.infrastructure.Database.contracts import DataContract


    # j.w. + dekorator + profil to przypał
    # jeśli chcesz mieć dedykowaną metodę do "insert profile to wtedy"
    # def insert_profile(self, profile: Profile) -> None:
    # jeśli chcesz mieć metodę do UMIESZCZANIA DANYCH to wtedy:
    # def insert_data(self, data: Data) -> None:
    # GDZIE Data to jest jakiś Protocol który ma metodę nwm: to_dict / to_binary / to_tuple
    # i wtedy nie wiesz czym jest data, jedyne co potrzebujesz to użyć pod spodem jej metody to_dict
    # OGROMNA różnica polega na tym, że w przypadku Profile -> Twoja klasa wie czym jest profil, co to za obiekt
    # w przypadku "DATA" on tylko wie, że przedstawiciel ten klasy ma zawarty kontrakt w postaci "HEJ MAM METODE TO_DICT"
    # w przypadku "Profile" on dokładnie zna calutką definicję klasy, przez co jest z nią ŚCIŚLE powiązany\



    # <- to możesz zrobić w inicie, potem w dekoratorze tylko obsługiwać wyjątek, jakby sesja wygasła to na
        # to jest najprawilniejsze podejście przemyśl je sam prosze.
        # on init -> stwórz połączenie
        # przy próbie inserta, użyj połączenia
        # jak połączenie jest aktywne, to go użyje i elo
        # jak połączenie jest nie aktywne, to je ponowi
        # zakład pascala, jak jest, nie tracisz czasu
        # jak nie ma połączenia to i tak musisz je stworzyć -> masz mniej niezbędnych operacji
        # w takim przypadku nie zamykaj połączenia

class DatabaseClient: 

    _tables ={"users": {
        "columns": ("nazwa","rating")
    }
    }


    def __init__(self, DB_URL: str):
        self.db_url: str = DB_URL
        self.engine = create_engine(self.db_url, connect_args={"connect_timeout": 30}, pool_pre_ping = True)
        self.session_factory = sessionmaker(bind=self.engine)

        self.session: Session =  self.session_factory()

 
    def _database_connection_decorator(func):
        def wrapper(self,*args,**kwargs):
            if self.session is None:
                self.session = self.session_factory()

            try:
                return func(self, *args, **kwargs)
            except OperationalError:
                self.session.close()
                self.session = self.session_factory()
                return func(self, *args, **kwargs)
            
        return wrapper

    def _columns_extractor(self, columns: Tuple[str]) -> str:

        result: str = ""
        result = ", ".join(columns)

        return result 

    def _keys_extractor(self, values: Dict[str, str | int]) -> str:
        values_keys_list: List[str] = []

        for key in values.keys():
            values_keys_list.append(f":{key}")

        result: str = ""
        result = ", ".join(values_keys_list)

        return result

    def _insert_user_data(self, table_name: str, columns: Tuple[str], values: Dict[str, str |int ]) -> str:
        values_bind: str = self._keys_extractor(values)
        columns_bind = self._columns_extractor(columns)

        if table_name not in self._tables:
            raise ValueError("Table name not found")
        
        
        return  f"""INSERT INTO {table_name} ({columns_bind}) 
                VALUES ({values_bind}) 
                ON CONFLICT (nazwa) 
                DO UPDATE SET rating = EXCLUDED.rating"""
        
    
    def _sort_users_by_rating(self,asc_or_desc: str) -> str:

       return  f"SELECT * FROM users ORDER BY rating {asc_or_desc}"""

    def _delete_user_by_username(self,table_name, column: Tuple[str]):
        if table_name not in self._tables:
            raise ValueError("Table name not found")

        single_column = column[0]

  

        return f"""DELETE FROM {table_name} WHERE {single_column} = :proper_username"""  #table_name = users, WHERE nazwa = ':value'""""

   
    def _show_all(self,table_name):
        return f"""SELECT * FROM {table_name}"""

    @_database_connection_decorator
    def insert_user_data(self, data: DataContract) -> None:
            self.session.execute(text(self._insert_user_data("users",self._tables["users"]["columns"],data.to_dict())),data.to_dict())
            self.session.commit() 

    @_database_connection_decorator
    def get_users(self) -> List[Profile]:
        result = self.session.execute(text(self._show_all("users"))).fetchall()
        profiles_list: List[Profile] = []
        for nazwa,rating in result:
            profiles_list.append(Profile(nazwa = nazwa, rating = rating))

        return profiles_list


    @_database_connection_decorator
    def delete_user_by_username(self,username: str) -> None:
        proper_username = username.lower()
        self.session.execute(text(self._delete_user_by_username("users",self._tables["users"]["columns"])),{"proper_username": proper_username})
        self.session.commit() 

    
    @_database_connection_decorator
    def sorting_users_by_rating(self,asc_or_desc: str ) -> List[Profile]:
        result = self.session.execute(text(self._sort_users_by_rating(asc_or_desc)),{"asc_or_desc":asc_or_desc}).fetchall()

        profiles_list: List[Profile] = []

        for nazwa,rating in result:
            profiles_list.append(Profile(nazwa=nazwa,rating=rating)) 

        return result
    