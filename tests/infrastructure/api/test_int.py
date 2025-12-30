from chess_rating.infrastructure.api.client import ApiClient
import pytest

api_client = ApiClient()

def test_api_response():
    username: str = "niedziaek"
    response = api_client.get(username)
    rating = response[username]
    

    
    assert rating == 587


    
def test_user_not_found():
    with pytest.raises(Exception) as wyjatek:
        api_client.get("pieseczekjekupsko")


def test_chess_rapid_not_found():
    with pytest.raises(Exception) as wyjatek:
        api_client.get("dwadaw")