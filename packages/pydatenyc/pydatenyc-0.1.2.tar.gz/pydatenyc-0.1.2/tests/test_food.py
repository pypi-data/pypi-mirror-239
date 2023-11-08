import pytest
import unittest
from pydate.food import food
from unittest import mock
from unittest.mock import patch, mock_open
import json

def test_valid_inputs():
    result = food(cuisine="French", price_range="Medium", meal="Dinner")
    assert "Recipe Name:" in result

def test_invalid_inputs():
    result = food(cuisine=123, price_range=True, meal="Dinner")
    assert result == "Your filter is invalid. Try again."

def test_no_matching_foods():
    result = food(cuisine="Italian", price_range="Luxury", meal="Midnight")
    assert result == "No food meets your requirements. Try again."

def test_matching_foods():
    result = food(cuisine="French", price_range="Medium", meal="Dinner")
    assert "Recipe Name:" in result

def test_matching_foods_case_insensitive():
    result1 = food(cuisine="french", price_range="medium", meal="dinner")
    result2 = food(cuisine="french", price_range="MEDIUM", meal="DINNER")
    result3 = food(cuisine="FRENCH", price_range="medium", meal="dinner")
    assert "Recipe Name:" in result1 and result2 and result3

def test_food_with_mock_data():
    mock_data = [
        {"name": "Fries", "cuisine": "American", "price_range": "low", "meal": "lunch"},
        {"name": "Burger", "cuisine": "American", "price_range": "low", "meal": "breakfast"},
        {"name": "Hot Pot", "cuisine": "Chinese", "price_range": "medium", "meal": "lunch"},
        {"name": "Pizza", "cuisine": "Italian", "price_range": "low", "meal": "dinner"},
    ]

    with patch('builtins.open', mock_open(read_data=json.dumps(mock_data))):
        
        with patch('random.choice', return_value=mock_data[0]):
            result = food(cuisine="American", price_range="low", meal="lunch")
    
    assert "Recipe Name: Fries" in result

if __name__ == "__main__":
    pytest.main()
