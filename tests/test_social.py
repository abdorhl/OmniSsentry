import pytest
from unittest.mock import patch
from omnissentry.core.social_media import social_media_scrape, SOCIAL_PLATFORMS

def test_social_platform_list():
    assert 'twitter' in SOCIAL_PLATFORMS
    assert 'github' in SOCIAL_PLATFORMS
    
@patch('omnissentry.core.social_media.requests.get')
def test_social_media_scrape(mock_get):
    # Mock the response
    mock_response = type('MockResponse', (), {'status_code': 200, 'text': '<html><body>Test</body></html>'})
    mock_get.return_value = mock_response
    
    # Using a common username
    result = social_media_scrape("test")
    assert isinstance(result, dict)
    assert len(result) == len(SOCIAL_PLATFORMS)
    
    # Check that each platform is returned in the results
    for platform in SOCIAL_PLATFORMS:
        assert platform in result
        assert result[platform]['exists'] == True  # All should be marked as existing with our mock
