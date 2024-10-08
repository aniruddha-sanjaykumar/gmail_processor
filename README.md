# Gmail Processor

A standalone Python script that integrates with the Gmail API and performs rule-based operations on emails.

## Prerequisites
1. Python 3.x
2. Google Cloud project with Gmail API enabled
3. credentials.json OAuth credentials

## Setup Instructions
### 1. Enable Gmail API and Obtain OAuth Credentials

#### Step 1: Enable the Gmail API:

a) Visit the Google Cloud Console. 

b) Create a new project or select an existing one. 

c) Navigate to APIs & Services > Library. 

d) Search for "Gmail API" and click Enable.

#### Step 2: Create OAuth 2.0 Credentials:

a) Go to APIs & Services > Credentials.

b) Click Create Credentials and choose OAuth 2.0 Client IDs.

c) Configure the consent screen (if prompted).
    
d) Select Desktop App as the application type. 

e) Download the credentials.json file and place it in the root directory.

### 2. Install Required Python Libraries

Create a virtual env and install the necessary dependencies using pip:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Define Rules in examples/rules.json

The rules for processing emails are defined in a rules.json file. Some sample rules are available in examples folder.

Rules format:

a) Predicate: Can be All (all conditions must match) or Any (any condition can match).

b) Fields: Conditions based on from, subject, snippet, received.

c) Actions: Actions include mark_as_read, mark_as_unread, or move.

### 4. Run the Script

#### Step 1: Running the Script:

From the root directory, run:

`python main.py`

#### Step 2: Authenticate with Google:

a) The first time you run the script, a browser will open for you to authenticate your Gmail account and grant permissions to the Gmail API. 

b) After successful authentication, a token.json file will be created for future use.

### 5. Testing

#### Steps to run pytests:

1. Install the dependencies in the project venv created earlier.
```bash
pip install -r test_requirements.txt
```
2. Run `pytest` command from the repo's root directory.

### 6. Manual Verification
Once the script runs:

a) Emails are fetched from your Gmail inbox and stored in an emails.db SQLite database. 

b) The script applies the rules defined in rules.json. 

c) Actions such as marking emails as read/unread or moving them to a specific label will be executed.

### 7. Handling Labels for the "Move" Action

If your rules include the move action, you can create the label (e.g., "Processed") for better UI experience:

a) Open Gmail 

b) Scroll down on the left sidebar, click More > Create new label.

c) Name the label (e.g., "Processed").

### File Summary

a) main.py: The main Python script. 

b) credentials.json: OAuth credentials for authenticating with Gmail API. 

c) rules.json: JSON file containing rules for email processing. 

d) emails.db: SQLite database file generated by the script to store emails.

### Troubleshooting

a) Authentication Errors: Ensure the credentials.json file is correctly placed and authenticate on the first run. 

b) Dependency Issues: Ensure all required Python libraries are installed 
(google-api-python-client, google-auth-httplib2, google-auth-oauthlib, sqlalchemy). 

c) API Quotas: Gmail API has rate limits, be mindful if processing many emails. 

d) Modifying Rules: Update rules.json to experiment with different rules and actions.