from mail_handler import GmailHandler
from db_handler import EmailDatabase
from rule_handler import load_rules, process_email
from config import RULE_PATH


def main():
    # Create an instance of GmailHandler
    gmail_handler = GmailHandler()

    # Initialize the database
    db = EmailDatabase()

    # Fetch and store emails
    emails = gmail_handler.fetch_emails()
    for email in emails:
        email_id = email['id']
        email_data = gmail_handler.get_email_data(email_id)
        # print("Email data", email_data)
        db.store_email(email_id, email_data)

    # Load rules
    rules = load_rules(RULE_PATH)

    # Fetch all emails from database
    all_emails = db.fetch_all_emails()
    # print(all_emails)

    # Fetch emails from database and process each one
    for email_data in all_emails:
        process_email(email_data, rules, gmail_handler)

    db.close_connection()


if __name__ == '__main__':
    main()
