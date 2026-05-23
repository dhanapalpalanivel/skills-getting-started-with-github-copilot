"""
Test suite for the GET /activities endpoint.

Tests verify that:
- Activities can be successfully retrieved
- The response contains all required fields for each activity
"""


def test_get_activities_success(client, reset_activities):
    """
    Test successful retrieval of all activities.
    
    Verifies that the /activities endpoint returns a 200 status code
    and returns a dictionary of activities.
    
    Uses AAA (Arrange-Act-Assert) pattern:
    - Arrange: Setup the test (no special setup needed)
    - Act: Make a GET request to /activities
    - Assert: Verify the response status and structure
    """
    # Arrange: No special setup needed for this test
    
    # Act: Make the GET request
    response = client.get("/activities")
    
    # Assert: Verify the response
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert len(response.json()) > 0


def test_get_activities_has_required_fields(client, reset_activities):
    """
    Test that the activities response contains all required fields.
    
    Verifies each activity in the response has:
    - name (implicit as dictionary key)
    - description
    - schedule
    - max_participants
    - participants
    
    Uses AAA (Arrange-Act-Assert) pattern:
    - Arrange: Define required fields
    - Act: Make a GET request and extract activities
    - Assert: Verify each activity has all required fields
    """
    # Arrange: Define the required fields for each activity
    required_fields = {"description", "schedule", "max_participants", "participants"}
    
    # Act: Get all activities
    response = client.get("/activities")
    activities_data = response.json()
    
    # Assert: Verify each activity has all required fields
    assert response.status_code == 200
    
    for activity_name, activity_info in activities_data.items():
        # Verify activity name is a string
        assert isinstance(activity_name, str)
        assert len(activity_name) > 0
        
        # Verify all required fields are present
        for field in required_fields:
            assert field in activity_info, f"Activity '{activity_name}' missing field '{field}'"
        
        # Verify field types
        assert isinstance(activity_info["description"], str)
        assert isinstance(activity_info["schedule"], str)
        assert isinstance(activity_info["max_participants"], int)
        assert isinstance(activity_info["participants"], list)
        
        # Verify participants are email strings
        for participant in activity_info["participants"]:
            assert isinstance(participant, str)
            assert "@" in participant  # Basic email validation
