"""
Test suite for the DELETE /activities/{activity_name}/unregister endpoint.

Tests verify that:
- Students can successfully unregister from activities
- Appropriate errors are returned for invalid operations
- Only registered students can unregister
"""


def test_unregister_success(client, reset_activities):
    """
    Test successful unregistration from an activity.
    
    Verifies that a student can unregister from an activity they are
    registered for and receives a 200 status code with a success message.
    
    Uses AAA (Arrange-Act-Assert) pattern:
    - Arrange: Select an activity with existing participants
    - Act: Make a DELETE request to unregister a student
    - Assert: Verify the response status and message
    """
    # Arrange: Use an existing participant from an activity
    activity_name = "Chess Club"
    student_email = "michael@mergington.edu"  # Exists in Chess Club participants
    
    # Act: Unregister the student
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": student_email}
    )
    
    # Assert: Verify successful unregistration
    assert response.status_code == 200
    assert "message" in response.json()
    assert student_email in response.json()["message"]
    assert activity_name in response.json()["message"]


def test_unregister_activity_not_found(client, reset_activities):
    """
    Test unregistration from a non-existent activity.
    
    Verifies that attempting to unregister from an activity that doesn't exist
    returns a 404 error with an appropriate message.
    
    Uses AAA (Arrange-Act-Assert) pattern:
    - Arrange: Define a non-existent activity name
    - Act: Attempt to unregister from the non-existent activity
    - Assert: Verify the 404 error response
    """
    # Arrange: Define test data with a non-existent activity
    activity_name = "Non-Existent Activity"
    student_email = "student@mergington.edu"
    
    # Act: Attempt to unregister from non-existent activity
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": student_email}
    )
    
    # Assert: Verify 404 error
    assert response.status_code == 404
    assert "detail" in response.json()
    assert "not found" in response.json()["detail"].lower()


def test_unregister_not_registered(client, reset_activities):
    """
    Test unregistration when student is not registered for activity.
    
    Verifies that attempting to unregister a student who is not registered
    for an activity returns a 400 error with an appropriate message.
    
    Uses AAA (Arrange-Act-Assert) pattern:
    - Arrange: Select an activity and a student not in its participants
    - Act: Attempt to unregister the non-registered student
    - Assert: Verify the 400 error response
    """
    # Arrange: Use an activity and a student not registered for it
    activity_name = "Chess Club"
    student_email = "notregistered@mergington.edu"  # Not in Chess Club participants
    
    # Act: Attempt to unregister a non-registered student
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": student_email}
    )
    
    # Assert: Verify 400 error for non-registered student
    assert response.status_code == 400
    assert "detail" in response.json()
    assert "not registered" in response.json()["detail"].lower()
