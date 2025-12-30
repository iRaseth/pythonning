import pytest
from unittest.mock import MagicMock, Mock
from chess_rating.infrastructure.Database.dataBaseClient import DatabaseClient
from chess_rating.infrastructure.Database.profile import Profile
from chess_rating.infrastructure.api.client import ApiClient


def test_insert_data():
    DatabaseClient._instance = None

    db = DatabaseClient("postgresql://dummy")
    mock_conn = MagicMock()
    db.engine = MagicMock()