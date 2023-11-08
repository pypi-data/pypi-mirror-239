import pytest
from pydate.pickupline import pickupline
from unittest import mock

def test_pickupline_valid_input_true():
    result = pickupline(text=True, category="Funny")
    assert "Here's Your Pick Up Line" in result

def test_pickupline_valid_input_false():
    result = pickupline(text=False, category="Funny")
    assert "Here's Your Pick Up Line" in result

def test_pickupline_invalid_input():
    result = pickupline(text="Bob")
    assert result == "The text flag must be a boolean. Try again."

def test_pickupline_category_no_match():
    result = pickupline(text=True, category="Spiderman")
    assert result == "I'm sorry. We didn't find any pick up lines matching your criteria. Try changing the category or text type."

def test_matching_categories_case_insensitive():
    result1 = pickupline(text=True, category="Funny")
    result2 = pickupline(text=True, category="funny")
    result3 = pickupline(text=True, category="FUNNY")
    assert "Here's Your Pick Up Line" in result1 and result2 and result3

def test_activity_with_mocked_data():
    
    with mock.patch('pydate.activities.json.load') as mock_json_load:
        mock_json_load.return_value = [
            {
    "pick_up_line": "Do you have an Instagram? My mom said she wants to follow our relationship. 📷",
    "suitable_for_text": True,
    "categories": ["Modern", "Funny"]
    },{
      "pick_up_line": "I'm not a mathematician, but I'm pretty good with numbers. Tell you what, give me yours and watch what I can do with it.",
      "suitable_for_text": False,
      "categories": ["Confident", "Clever", "Funny"]
    },{
      "pick_up_line": "I was blinded by your beauty; I'm going to need your name and number for insurance purposes.",
      "suitable_for_text": False,
      "categories": ["Humorous", "Clever"]
    }
        ]
        result = pickupline(text=True, category="FUNNY")
        assert "Do you have an Instagram?" in result

# Run the tests
if __name__ == "__main__":
    pytest.main()