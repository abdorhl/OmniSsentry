import pytest
from unittest.mock import patch, MagicMock
from omnissentry.core.email_osint import validate_email, email_osint_full

def test_email_validation():
    assert validate_email("user@example.com") == True
    assert validate_email("invalid-email") == False
    assert validate_email("user@domain") == False
    
@patch('omnissentry.core.email_osint.requests.get')
def test_email_osint_full(mock_get):
    # Mock response for requests
    mock_response = MagicMock()
    mock_response.json.return_value = {"data": {"result": "deliverable"}}
    mock_get.return_value = mock_response
    
    result = email_osint_full("test@example.com")
    assert isinstance(result, dict)
    assert "error" not in result or result["error"] != "Invalid email format"
