from pydate.dessert import dessert
from unittest.mock import patch
import pytest

mock_shops_data = [
    {
      "name": "Venchi",
      "price": "high",
      "type": "frozen"
    },
    {
      "name": "M&M's New York",
      "price": "low",
      "type": "candy"
    }
]

@pytest.fixture
def mock_json_load():
    with patch("json.load") as mock_load:
        mock_load.return_value = mock_shops_data
        yield mock_load

@pytest.fixture
def mock_random_choice():
    with patch("random.choice") as mock_choice:
        mock_choice.return_value = mock_shops_data[0]
        yield mock_choice

def test_dessert_found(mock_json_load, mock_random_choice):
    result = dessert("frozen", "high")
    assert "Venchi" in result

def test_dessert_type_not_found(mock_json_load, mock_random_choice):
    result = dessert("pastry", "medium")
    assert "Oops, no desserts found" in result

def test_no_desserts_found(mock_json_load, mock_random_choice):
    mock_json_load.return_value = []
    result = dessert("bakery", "medium")
    assert "Oops, no desserts found" in result
