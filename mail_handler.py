import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from config import SCOPES, LABEL


class GmailHandler:
    """
    Class to handle Gmail API operations such as authentication, fetching
    emails, and extracting email data.
    """

    def __init__(self):
        """
        Initializes the GmailHandler instance by authenticating the Gmail
        service.
        """
        self.service = self.authenticate_gmail()

    def authenticate_gmail(self):
        """
        Authenticates the Gmail API using OAuth2. If token.json exists, it
        will use stored credentials; otherwise, it will initiate a login flow
        and store new credentials in token.json.

        Returns:
        - service (googleapiclient.discovery.Resource): Authenticated Gmail
            API service.
        """
        creds = None

        # The token.json stores the user's access and refresh tokens.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json',
                                                          SCOPES)

        # If no valid credentials, ask the user to log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.\
                    from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)

            # Save the credentials for future use
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        # Return the authenticated Gmail service
        return build('gmail', 'v1', credentials=creds)

    def fetch_emails(self, max_results=10):
        """
        Fetches a list of emails from the user's Gmail inbox.

        Args:
        - max_results (int): Maximum number of emails to fetch. Default is 10.

        Returns:
        - list: A list of email message objects retrieved from the inbox.
        """
        try:
            # Fetch email messages from the 'INBOX' label
            results = self.service.users().messages().\
                list(userId='me', labelIds=['INBOX'],
                     maxResults=max_results).execute()
            messages = results.get('messages', [])
            return messages
        except Exception as e:
            print(f"An error occurred while fetching emails: {e}")
            return []

    def get_email_data(self, message_id):
        """
        Retrieves detailed information about a specific email, including its
        subject, sender, date, and snippet.

        Args:
        - message_id (str): The unique ID of the email message.

        Returns:
        - dict: A dictionary containing the email's subject, sender, date,
                and snippet.
        """
        try:
            # Retrieve the email message by its ID
            message = self.service.users().messages().\
                get(userId='me', id=message_id).execute()
            payload = message['payload']
            headers = payload['headers']

            # Extract relevant headers: Subject, From, Date
            email_data = {}
            for header in headers:
                if header['name'] == 'Subject':
                    email_data['subject'] = header['value']
                if header['name'] == 'From':
                    email_data['from'] = header['value']
                if header['name'] == 'Date':
                    email_data['date'] = header['value']

            # Add email snippet to the data
            email_data['snippet'] = message['snippet']
            return email_data
        except Exception as e:
            print(f"An error occurred while retrieving email data for message "
                  f"ID {message_id}: {e}")
            return {}

    def mark_as_read(self, email_data):
        """
        Mark the email as read using the Gmail API.
        """
        email_id = email_data['id']
        self.service.users().messages(). \
            modify(userId='me', id=email_id,
                   body={'removeLabelIds': ['UNREAD']}).execute()

    def mark_as_unread(self, email_data):
        """
        Mark the email as unread using the Gmail API.
        """
        email_id = email_data['id']
        self.service.users().messages(). \
            modify(userId='me', id=email_id,
                   body={'addLabelIds': ['UNREAD']}).execute()

    def move_email(self, email_data, label_name=LABEL):
        """
        Move the email to a different folder using the Gmail API.
        """
        # List all existing labels
        labels = self.list_labels()
        label_ids = [label['id'] for label in labels if
                     label['name'].lower() == label_name.lower()]
        # If the label doesn't exist, create it
        if not label_ids:
            created_label = self.create_label(label_name)
            if created_label:
                label_id = created_label['id']
            else:
                print(f"Failed to create label: {label_name}")
                return
        else:
            label_id = label_ids[0]

        # Now apply the label to the email
        try:
            email_id = email_data['id']
            subject = email_data['subject']
            self.service.users().messages().\
                modify(userId='me', id=email_id,
                       body={'addLabelIds': [label_id]}).execute()
            print(f"Label '{label_name}' applied to email with "
                  f"Subject: {subject}.")
        except Exception as e:
            print(f"An error occurred while applying label '{label_name}': {e}")

        # email_id = email_data['id']
        # # Replace with your label ID
        # label_id = label
        # self.service.users().messages(). \
        #     modify(userId='me', id=email_id,
        #            body={'addLabelIds': [label_id]}).execute()

    def list_labels(self):
        """List all labels in the user's Gmail account."""
        try:
            results = self.service.users().labels().list(userId='me').execute()
            labels = results.get('labels', [])
            if not labels:
                print('No labels found.')
                return []
            else:
                return labels
        except Exception as e:
            print(f"An error occurred while fetching labels: {e}")
            return []

    def create_label(self, label_name):
        """Create a new label in the user's Gmail account."""
        label = {
            'labelListVisibility': 'labelShow',
            'messageListVisibility': 'show',
            'name': label_name
        }
        try:
            created_label = self.service.users().labels().\
                create(userId='me', body=label).execute()
            print(f"Label '{label_name}' created.")
            return created_label
        except Exception as e:
            print(f"An error occurred while creating the label '{label_name}': {e}")
            return None

