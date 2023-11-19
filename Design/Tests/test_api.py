import requests

from underground import feed, metadata

def test_request_invalid_feed():
    """Test that request raises value error for an invalid feed."""
    with pytest.raises(ValueError):
        feed.request("NOT REAL")
