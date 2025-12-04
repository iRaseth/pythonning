from httpx import Client

class ApiClient:
    BASE_URL = "https://dupadupa2137dupa.com"

    def __init__(self) -> None:
        self._client = Client(
            base_url=self.BASE_URL
        )
    
    def get(self, endpoint: str, username: str) -> dict:
        response = self._client.get(endpoint)
        return response
