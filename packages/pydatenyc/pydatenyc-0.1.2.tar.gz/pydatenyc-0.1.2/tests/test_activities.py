import pytest
import unittest
from pydate.activities import activity
from unittest import mock

def test_activity_valid_input():
    result = activity(indoor=True, time="evening")
    assert isinstance(result, str)

def test_activity_invalid_input():
    result = activity(indoor="invalid", time=123)
    assert result == "Your filter is invalid. Try again."

def test_activity_no_match():
    result = activity(indoor=True, time="midnight")
    assert result == "Stay home and relax."

def test_matching_activities_case_insensitive_time():
    result1 = activity(indoor=True, time="EVENING")
    result2 = activity(indoor=True, time="Evening")
    result3 = activity(indoor=True, time="evening")
    assert "Activity:" in result1 and result2 and result3

def test_activity_with_mocked_data():
    
    with mock.patch('pydate.activities.json.load') as mock_json_load:
        mock_json_load.return_value = [
            {"activity": "Soccer", "indoor": True, "time": "morning"},
            {"activity": "Basketball", "indoor": False, "time": "evening"},
            {"activity": "Table Tennis", "indoor": False, "time": "morning"},
            {"activity": "Reading", "indoor": True, "time": "evening"},
        ]
        result = activity(indoor=True, time="evening")
        assert "Activity: Reading" in result

# Run the tests
if __name__ == "__main__":
    pytest.main()
