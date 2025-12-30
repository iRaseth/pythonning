from chess_rating.infrastructure.api.client import ApiClient, Client
from chess_rating.infrastructure.Database.profile import Profile
from pytest_httpx import HTTPXMock
from unittest.mock import MagicMock
import httpx
import pytest
from typing import Dict

def test_api_client_get(httpx_mock: HTTPXMock) -> None:
    # GIVEN
    # Tu se tworzymy obiekt ktorego metody bedziemy testowac
    api_client = ApiClient()
    # Tu se mowimy pajtonowi:
    # WSZYSTKO CO IDZIE NA TA SCIEZKIE TO NORMALNIE OD BUTA UDAJEMY ZE JESTESMY
    # PRAWDZIWYM API I ZWRACAMY SE CO CHCEMY
    httpx_mock.add_response(url= "https://api.chess.com/pub/player/belmondziak/stats", method="GET", status_code=200, json={"chess_rapid": {
        "last":{
            "rating": 213
        }
    }})

    # WHEN
    res = api_client.get("belmondziak")

    # THEN
    assert res == {"belmondziak": 213}
    assert 213 == res["belmondziak"] 
 


def test_api_client_rating_not_found(httpx_mock: HTTPXMock) -> None:
    api_client = ApiClient()
    result: Dict [str,int ] = {}
    httpx_mock.add_response(url= "https://api.chess.com/pub/player/belmondziak/stats", method="GET", status_code=200, json={"chess_blitz": {
        "last": {
            "rating": 213
        }
    }})
    # THEN
    with pytest.raises(Exception) as wyjatek:  
        result = api_client.get("belmondziak")

    assert str(wyjatek.value) == "Uzytkownik nie ma rankingu na rapidach"
 