import pytest
import sqlite3
from db_handler import EmailDatabase


@pytest.fixture(scope='function')
def email_db():
    """
    Fixture to provide a clean test database before each test,
    and remove it after the test completes.
    """
    db = EmailDatabase(db_name=':memory:')  # Use in-memory database for testing
    yield db
    db.close_connection()


def test_setup_db(email_db):
    """
    Test that the 'emails' table is created successfully in the database.
    """
    cursor = email_db.conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='emails';")
    result = cursor.fetchone()
    assert result is not None, "Emails table should be created"


def test_store_email(email_db):
    """
    Test that an email is stored successfully in the database.
    """
    email_data = {
        'subject': 'Test Subject',
        'from': 'test@example.com',
        'snippet': 'This is a test email.',
        'date': '2024-10-06'
    }
    email_db.store_email('1', email_data)

    # Check if the email is stored correctly
    cursor = email_db.conn.cursor()
    cursor.execute("SELECT * FROM emails WHERE id = ?", ('1',))
    result = cursor.fetchone()

    assert result is not None, "Email should be stored in the database"
    assert result[1] == 'Test Subject', "Subject should match"
    assert result[2] == 'test@example.com', "Sender should match"
    assert result[3] == 'This is a test email.', "Snippet should match"
    assert result[4] == '2024-10-06', "Date should match"


def test_fetch_all_emails(email_db):
    """
    Test that emails can be fetched as a list of dictionaries from the database.
    """
    # Insert multiple email records
    email_data_1 = {
        'subject': 'First Test Email',
        'from': 'first@example.com',
        'snippet': 'Snippet 1',
        'date': '2024-10-01'
    }
    email_data_2 = {
        'subject': 'Second Test Email',
        'from': 'second@example.com',
        'snippet': 'Snippet 2',
        'date': '2024-10-02'
    }
    email_db.store_email('1', email_data_1)
    email_db.store_email('2', email_data_2)

    # Fetch all emails
    emails = email_db.fetch_all_emails()

    assert len(emails) == 2, "There should be 2 emails in the database"
    assert emails[0]['subject'] == 'First Test Email', "First email's subject should match"
    assert emails[1]['from'] == 'second@example.com', "Second email's sender should match"


def test_close_connection(email_db):
    """
    Test that the database connection is closed successfully.
    """
    email_db.close_connection()
    with pytest.raises(sqlite3.ProgrammingError):
        email_db.conn.cursor().execute("SELECT 1")  # Connection should be closed
