import pytest
from mail_handler import GmailHandler


@pytest.mark.integration
def test_fetch_emails():
    gmail_handler = GmailHandler()
    messages = gmail_handler.fetch_emails()

    assert isinstance(messages, list), "Messages should be returned as a list"
    assert len(messages) > 0, "At least one email should be fetched"
    assert 'id' in messages[0], "Each message should contain an 'id' field"
