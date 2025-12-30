from httpx import Client
from typing import Dict


class ApiClient:
    BASE_URL = "https://api.chess.com/pub/player/"

    def __init__(self) -> None:
        self._client = Client(
            base_url=self.BASE_URL
        )
    
    def get(self,username: str) -> Dict:
        proper_username = username.lower()
        endpoint = f"/{proper_username}/stats"
        response = self._client.get(endpoint)

        if response.status_code != 200:
            raise Exception("Nie udalo sie znalezc uzytkownika")

        data = response.json()
        parsed: Dict[str,int] = {}

        if "chess_rapid" in data and "last" in data["chess_rapid"]:
            parsed[proper_username] = data["chess_rapid"]["last"]["rating"]
            return parsed
        else:
            raise Exception("Uzytkownik nie ma rankingu na rapidach")


    

