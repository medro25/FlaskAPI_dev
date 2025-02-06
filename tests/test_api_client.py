import pytest
from unittest.mock import patch, MagicMock
from services.api_client import LuxidAPIClient, get_api_client, token_cache

@pytest.fixture(autouse=True)
def clear_token_cache():
    """Automatically clears the token cache before each test."""
    token_cache.clear()
    
@pytest.fixture
def mock_client():
    """Creates a LuxidAPIClient instance for testing."""
    return LuxidAPIClient(username="test_user", password="test_pass")

@patch("services.api_client.requests.post")
def test_authenticate_success(mock_post, mock_client):
    """Test that authentication successfully retrieves and caches a token."""
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"token": "mocked_token"}

    mock_client.authenticate()
    
    # Verify token was cached
    assert token_cache["test_user"] == "mocked_token"

@patch("services.api_client.requests.post")
def test_authenticate_failure(mock_post, mock_client):
    """Test authentication failure when the API returns an error."""
    mock_post.return_value.status_code = 401

    with pytest.raises(Exception, match="Authentication failed: 401"):
        mock_client.authenticate()

@patch("services.api_client.requests.get")
def test_fetch_events_with_cached_token(mock_get, mock_client):
    """Test that fetching events works when a cached token is available."""
    # Simulate cached token
    token_cache["test_user"] = "mocked_token"

    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [{"event_id": "123"}]

    events = mock_client.fetch_events()

    # Ensure the API call was made with the correct headers
    mock_get.assert_called_once_with(
        "https://recruiment-api-1069519412575.europe-west3.run.app/events",
        headers={"Authorization": "Bearer mocked_token"}
    )
    
    assert events == [{"event_id": "123"}]

@patch("services.api_client.requests.get")
@patch("services.api_client.requests.post")
def test_fetch_events_with_expired_token(mock_post, mock_get, mock_client):
    """Test that a new token is requested when the old one is expired."""
    mock_get.return_value.status_code = 401  # Simulate expired token response

    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"token": "new_mocked_token"}

    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [{"event_id": "456"}]

    events = mock_client.fetch_events()

    # Ensure the token was refreshed
    assert token_cache["test_user"] == "new_mocked_token"

    # Ensure the second API request was made with the new token
    mock_get.assert_called_with(
        "https://recruiment-api-1069519412575.europe-west3.run.app/events",
        headers={"Authorization": "Bearer new_mocked_token"}
    )

    assert events == [{"event_id": "456"}]

@patch("services.api_client.requests.get")
def test_fetch_participants_success(mock_get, mock_client):
    """Test that fetching participants works with a valid token."""
    token_cache["test_user"] = "mocked_token"

    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"participant_id": "789"}

    participants_url = "https://api.example.com/events/participants/123"
    participants = mock_client.fetch_participants(participants_url)

    mock_get.assert_called_once_with(
        participants_url,
        headers={"Authorization": "Bearer mocked_token"}
    )

    assert participants == {"participant_id": "789"}

@patch("services.api_client.requests.get")
def test_fetch_participants_failure(mock_get, mock_client):
    """Test that fetching participants fails gracefully."""
    token_cache["test_user"] = "mocked_token"

    mock_get.return_value.status_code = 500

    participants_url = "https://api.example.com/events/participants/123"

    with pytest.raises(Exception, match="Failed to fetch participants: 500"):
        mock_client.fetch_participants(participants_url)

@patch("services.api_client.requests.post")
def test_get_api_client(mock_post):
    """Test that get_api_client correctly initializes the client."""
    client = get_api_client()
    assert isinstance(client, LuxidAPIClient)
