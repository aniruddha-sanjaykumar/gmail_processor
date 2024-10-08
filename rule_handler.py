from datetime import datetime
from dateutil import parser
import json


def load_rules(file_path):
    """
    Load the rules from a JSON file.
    """
    try:
        with open(file_path, 'r') as file:
            rules = json.load(file)
        return rules
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {file_path}: {e}")
        return None


def parse_email_date(date_str):
    """
    Generalize the date parsing by using dateutil.parser, which can handle
    various formats.
    """
    try:
        return parser.parse(date_str).date()
    except (ValueError, TypeError) as e:
        raise ValueError(f"Failed to parse date: {date_str}. Error: {e}")


def evaluate_condition(email_data, field, predicate, value):
    """
    Evaluate a single condition based on the email data, field, predicate,
    and value.
    """
    # Handle date fields
    if field == "received":
        email_date = parse_email_date(email_data['date'])
        value_date = datetime.strptime(value, '%Y-%m-%d').date()

        if predicate == "less than":
            return email_date < value_date
        elif predicate == "greater than":
            return email_date > value_date

    # Handle string fields (from, subject, message)
    email_field_value = email_data.get(field, "").lower()
    value = value.lower()

    if predicate == "contains":
        return value in email_field_value
    elif predicate == "does not contain":
        return value not in email_field_value
    elif predicate == "equals":
        return email_field_value == value
    elif predicate == "does not equal":
        return email_field_value != value

    return False


def evaluate_rules(email_data, rule_set):
    """
    Evaluate the rules in the rule_set. Since there's only one rule_set, the
    predicate 'All' or 'Any' is applied.
    """
    predicate = rule_set['predicate']
    rules = rule_set['rules']

    results = []
    for rule in rules:
        field = rule['field']
        pred = rule['predicate']
        value = rule['value']
        results.append(evaluate_condition(email_data, field, pred, value))

    if predicate == "All":
        return all(results)
    elif predicate == "Any":
        return any(results)

    return False


def process_email(email_data, rules_json, gmail_handler):
    """
    Process an email by evaluating it against the rules in the rules JSON.
    """
    if evaluate_rules(email_data, rules_json):
        actions = rules_json['actions']
        take_actions(email_data, actions, gmail_handler)


def take_actions(email_data, actions, gmail_handler):
    """
    Take actions such as marking the email as read or moving it.
    """
    for action in actions:
        if action == "mark_as_read":
            gmail_handler.mark_as_read(email_data)
        elif action == "mark_as_unread":
            gmail_handler.mark_as_unread(email_data)
        elif action == "move":
            gmail_handler.move_email(email_data)
