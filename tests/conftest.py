"""
Pytest configuration and fixtures for the activities API test suite.

This module provides:
- TestClient fixture for making HTTP requests to the API
- reset_activities fixture for resetting the activities state between tests
- Sample test data for consistent test scenarios
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


# Sample test data that represents the initial state of activities
SAMPLE_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Art Studio": {
        "description": "Explore painting, drawing, and mixed media art projects",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["mia@mergington.edu", "logan@mergington.edu"]
    },
    "Drama Club": {
        "description": "Develop acting skills and prepare for school performances",
        "schedule": "Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 20,
        "participants": ["eva@mergington.edu", "noah@mergington.edu"]
    }
}


@pytest.fixture
def client():
    """
    Fixture that provides a TestClient instance for making requests to the API.
    
    Returns:
        TestClient: A test client for the FastAPI application
    """
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """
    Fixture that resets the activities dictionary to its initial state before each test.
    
    This ensures test isolation by resetting the in-memory database between tests,
    preventing test interdependencies and ensuring consistent test behavior.
    
    Yields:
        None: Resets activities dict and yields control to the test
    """
    # Clear the current activities
    activities.clear()
    
    # Repopulate with sample data
    for activity_name, activity_data in SAMPLE_ACTIVITIES.items():
        # Create a deep copy to avoid shared references between tests
        activities[activity_name] = {
            "description": activity_data["description"],
            "schedule": activity_data["schedule"],
            "max_participants": activity_data["max_participants"],
            "participants": activity_data["participants"].copy()  # Shallow copy of list
        }
    
    # Yield control to the test
    yield
    
    # Cleanup after test (reset again for next test)
    activities.clear()
    for activity_name, activity_data in SAMPLE_ACTIVITIES.items():
        activities[activity_name] = {
            "description": activity_data["description"],
            "schedule": activity_data["schedule"],
            "max_participants": activity_data["max_participants"],
            "participants": activity_data["participants"].copy()
        }
