from chess_rating.infrastructure.api.client import ApiClient
from pytest_httpx import HTTPXMock
import httpx

def test_api_client_get(httpx_mock: HTTPXMock) -> None:
    # GIVEN
    # Tu se tworzymy obiekt ktorego metody bedziemy testowac
    api_client = ApiClient()
    # Tu se mowimy pajtonowi:
    # WSZYSTKO CO IDZIE NA TA SCIEZKIE TO NORMALNIE OD BUTA UDAJEMY ZE JESTESMY
    # PRAWDZIWYM API I ZWRACAMY SE CO CHCEMY
    httpx_mock.add_response(url="https://dupadupa2137dupa.com/dupa", method="GET")

    # WHEN
    res = api_client.get("/dupa", "dupa")

    # THEN
    ...