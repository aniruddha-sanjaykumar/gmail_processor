import sqlite3


class EmailDatabase:
    """
    Class to handle the database operations for storing and retrieving email
    data.
    """

    def __init__(self, db_name='emails.db'):
        """
        Initialize the connection to the SQLite database and set up the emails
        table.
        """
        self.conn = sqlite3.connect(db_name)
        self.setup_db()

    def setup_db(self):
        """
        Set up the 'emails' table in the database if it doesn't already exist.
        """
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS emails 
                          (id TEXT PRIMARY KEY, subject TEXT, sender TEXT, 
                          snippet TEXT, date TEXT)''')
        self.conn.commit()

    def store_email(self, email_id, email_data):
        """
        Insert or update an email record in the database.

        Args:
        - email_id (str): Unique ID of the email.
        - email_data (dict): Dictionary containing 'subject', 'from', 'snippet',
                            and 'date' of the email.
        """
        cursor = self.conn.cursor()
        cursor.execute('''INSERT OR REPLACE INTO emails (id, subject, sender, 
                            snippet, date) VALUES (?, ?, ?, ?, ?)''',
                       (email_id, email_data['subject'], email_data['from'],
                        email_data['snippet'], email_data['date']))
        self.conn.commit()

    def fetch_all_emails(self):
        """
        Retrieve all email records from the database and return them as a list
        of dictionaries.

        Returns:
        - list of dicts: Each dictionary contains the email data (id, subject,
                         sender, snippet, date).
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM emails")
        rows = cursor.fetchall()

        # Convert rows to a list of dictionaries. This functionality can be
        # split into a new function. For the simplicity of the demo, I have
        # combined them in to a single  function.

        emails = []
        for row in rows:
            # TODO: the following can be converted into a dataclass for better
            #  readability and re-usabilty
            email = {
                'id': row[0],
                'subject': row[1],
                'from': row[2],
                'snippet': row[3],
                'date': row[4]
            }
            emails.append(email)

        return emails

    def close_connection(self):
        """
        Close the database connection.
        """
        self.conn.close()
