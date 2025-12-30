from sqlalchemy import engine
from sqlalchemy import create_engine, text
from typing import Dict, List, Tuple
from chess_rating.infrastructure.Database.profile import Profile
from typing import Any, Protocol


class DatabaseClient: 
    def __init__(self, DB_URL: str):
        if self.initalized:
            return

        self.db_url: str = DB_URL
        self.engine = create_engine(self.db_url, connect_args={"connect_timeout": 30})
        self.initalized = True

    # pierwsze -> type hints
    # drugie -> camel_case
    # nie hardkoduj na pałe, wstrzykuj wartości
    # reszta do przerobienia również
    def _insert_data(self, table_name: str, columns: tuple[str], values: tuple[Any]) -> str:
        return (
            f"INSERT INTO {table_name} {columns} "
            f"VALUES {values} "
            "ON CONFLICT (nazwa) "
            "DO UPDATE SET rating = EXCLUDED.rating"
        )
    
    # j.w.
    def _deleteUser(self):        
        return text("DELETE FROM users WHERE nazwa = :proper_username")

    # j.w.
    def _get_users(self):
        return text(
                    "SELECT * FROM users"
                )

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

    class Data(BaseModel):
       x: int
       y: str
       dupa: str

       def to_dict() -> dict:
            ...
    
    class DataContract(Protocol): < uzywaj wszedzie
        def to_dict() -> dict:
            ...
    
    class Profile(BaseModel): < przenosiciel jakis danych, byc moze udostepnia swoj interfejs czyli funkcje
        a: str
        b: str
        c: str
    
        def to_dict() -> dict:
            ...
        
        def to_json() -> dict:
            ...

        def to_object() -> Self:
            ...

    def insertData(self, data: DataContract) -> None:
        conn = self.engine.connect()
        try:
            conn.execute(self._insertData(),profil.to_dict())
        finally:
            conn.commit() 
            conn.close()

    # j.w. + dekorator
    def get_users(self) -> List[Profile]:
        conn = self.engine.connect() 
        # <- to możesz zrobić w inicie, potem w dekoratorze tylko obsługiwać wyjątek, jakby sesja wygasła to na
        # to jest najprawilniejsze podejście przemyśl je sam prosze.
        # on init -> stwórz połączenie
        # przy próbie inserta, użyj połączenia
        # jak połączenie jest aktywne, to go użyje i elo
        # jak połączenie jest nie aktywne, to je ponowi
        # zakład pascala, jak jest, nie tracisz czasu
        # jak nie ma połączenia to i tak musisz je stworzyć -> masz mniej niezbędnych operacji
        # w takim przypadku nie zamykaj połączenia
        try: 
            result = conn.execute(self._get_users()).fetchall()
            profiles_list: List[Profile] = []
            for row in result:
                profiles_list.append(Profile(nazwa = row[0], rating = row[1]))
        finally:
            conn.close()
        return profiles_list

    # j.w.
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
