"""
Test suite for the POST /activities/{activity_name}/signup endpoint.

Tests verify that:
- Students can successfully sign up for activities
- Appropriate errors are returned for invalid operations
- Duplicate registrations are prevented
- Full activities are handled correctly
"""


def test_signup_success(client, reset_activities):
    """
    Test successful signup for an activity.
    
    Verifies that a student can sign up for an activity and receives
    a 200 status code with a success message.
    
    Uses AAA (Arrange-Act-Assert) pattern:
    - Arrange: Define test student email and activity name
    - Act: Make a POST request to sign up the student
    - Assert: Verify the response status and message
    """
    # Arrange: Define test data
    activity_name = "Chess Club"
    student_email = "newstudent@mergington.edu"
    
    # Act: Attempt to sign up the student
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": student_email}
    )
    
    # Assert: Verify successful signup
    assert response.status_code == 200
    assert "message" in response.json()
    assert student_email in response.json()["message"]
    assert activity_name in response.json()["message"]


def test_signup_activity_not_found(client, reset_activities):
    """
    Test signup for a non-existent activity.
    
    Verifies that attempting to sign up for an activity that doesn't exist
    returns a 404 error with an appropriate message.
    
    Uses AAA (Arrange-Act-Assert) pattern:
    - Arrange: Define a non-existent activity name
    - Act: Attempt to sign up for the non-existent activity
    - Assert: Verify the 404 error response
    """
    # Arrange: Define test data with a non-existent activity
    activity_name = "Non-Existent Activity"
    student_email = "student@mergington.edu"
    
    # Act: Attempt to sign up for non-existent activity
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": student_email}
    )
    
    # Assert: Verify 404 error
    assert response.status_code == 404
    assert "detail" in response.json()
    assert "not found" in response.json()["detail"].lower()


def test_signup_duplicate_registration(client, reset_activities):
    """
    Test signup when student is already registered.
    
    Verifies that attempting to sign up a student who is already registered
    for an activity returns a 400 error with an appropriate message.
    
    Uses AAA (Arrange-Act-Assert) pattern:
    - Arrange: Select an activity and use an existing participant
    - Act: Attempt to sign up the same student again
    - Assert: Verify the 400 error response
    """
    # Arrange: Use an existing participant from an activity
    activity_name = "Chess Club"
    student_email = "michael@mergington.edu"  # Already in Chess Club participants
    
    # Act: Attempt to sign up the student again (duplicate registration)
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": student_email}
    )
    
    # Assert: Verify 400 error for duplicate registration
    assert response.status_code == 400
    assert "detail" in response.json()
    assert "already signed up" in response.json()["detail"].lower()


def test_signup_activity_full(client, reset_activities):
    """
    Test signup when activity has reached maximum capacity.
    
    Verifies that attempting to sign up for an activity that has reached
    its maximum number of participants returns a 400 error.
    
    Uses AAA (Arrange-Act-Assert) pattern:
    - Arrange: Fill an activity to capacity by adding participants
    - Act: Attempt to sign up one more student
    - Assert: Verify the 400 error response
    """
    # Arrange: Get an activity and fill it to max capacity
    activity_name = "Art Studio"
    test_student = "fulltest@mergington.edu"
    
    # Access the activities dict directly to fill it for testing
    from src.app import activities
    
    # Get the max capacity
    max_participants = activities[activity_name]["max_participants"]
    current_participants = len(activities[activity_name]["participants"])
    
    # Fill the activity by adding fake participants if needed
    if current_participants < max_participants:
        for i in range(max_participants - current_participants):
            activities[activity_name]["participants"].append(f"filler{i}@mergington.edu")
    
    # Act: Attempt to sign up when activity is at capacity
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": test_student}
    )
    
    # Assert: Verify 400 error for full activity
    assert response.status_code == 400
    assert "detail" in response.json()
    # The error message might mention "full", "capacity", or "max_participants"
    error_detail = response.json()["detail"].lower()
    assert any(word in error_detail for word in ["full", "capacity", "maximum"])
