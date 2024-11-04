import csv
import random
import datetime
from faker import Faker
import time
from loguru import logger # Import logger

# Initialize faker for generating random data
fake = Faker()

# Define the list of headers
HEADERS = [
    "Summary", "Ticket key", "Ticket id", "Ticket Type", "Status", "Project key", "Project name", "Project type",
    "Project lead", "Project description", "Project url", "Priority", "Resolution", "Assignee", "Reporter", "Creator",
    "Created", "Updated", "Last Viewed", "Resolved", "Affects Version/s", "Fix Version/s", "Component/s", "Due Date",
    "Votes", "Labels", "Description", "Environment", "Watchers", "Log Work", "Original Estimate",
    "Remaining Estimate", "Time Spent", "Work Ratio", "Σ Original Estimate", "Σ Remaining Estimate",
    "Σ Time Spent", "Security Level", "Attachment", "Custom field (% Executed)", "Comment"
]

# Define some sample data
PROJECT_KEYS = ["MFS"]
PROJECT_NAMES = ["Moon Flight System"]
TICKET_TYPES = ["Bug", "Improvement", "Task", "New Feature"]
STATUSES = ["Open", "In Progress", "Closed", "Reopened"]
PRIORITIES = ["Low", "Medium", "High", "Critical"]
RESOLUTIONS = ["Fixed", "Won't Fix", "Duplicate", "Incomplete"]
COMPONENTS = ["Core", "UI", "Backend", "Integration"]
LABELS = ["label1", "label2", "label3", "label4"]

# Format for generated date strings
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Generate random ticket key
def generate_ticket_key(project_key, ticket_id):
    return f"{project_key}-{ticket_id}"

# Generate random date string
def random_date(start, end):
    start_date = datetime.datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end, "%Y-%m-%d")
    return fake.date_time_between(start_date=start_date, end_date=end_date).strftime(DATE_FORMAT)

# Generate random data for each field
def generate_ticket(ticket_id):
    project_key = random.choice(PROJECT_KEYS)
    project_name = random.choice(PROJECT_NAMES)
    ticket_type = random.choice(TICKET_TYPES)
    status = random.choice(STATUSES)
    priority = random.choice(PRIORITIES)
    resolution = random.choice(RESOLUTIONS)
    summary = fake.sentence()
    description = fake.text()
    environment = fake.sentence()
    assignee = fake.user_name()
    reporter = fake.user_name()
    creator = fake.user_name()
    created = random_date("2023-09-01", "2023-09-30")
    updated = random_date("2023-09-01", "2023-10-30")
    resolved = random_date("2023-09-01", "2023-10-30") if status == "Closed" else ""
    return [
        summary, generate_ticket_key(project_key, ticket_id), ticket_id, ticket_type, status, project_key, project_name, "software",
        assignee, f"{project_name} software project", fake.url(), priority, resolution, assignee, reporter, creator,
        created, updated, "", resolved, random.choice(LABELS), random.choice(LABELS), random.choice(COMPONENTS), random_date("2023-11-01", "2023-12-31"),
        random.randint(0, 10), random.choice(LABELS), description, environment, assignee, "", "", "", "", "",
        "", "", "", "", "", "", "", "", status, "", "", "", random.choice(LABELS), "", random.choice(LABELS), description
    ]

# Generate specified number of tickets
def generate_tickets(n):
    tickets = []
    for ticket_id in range(1, n + 1):
        tickets.append(generate_ticket(ticket_id))
    return tickets

# Save tickets to CSV file
def save_to_csv(filename, tickets):
    with open(filename, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(HEADERS)
        writer.writerows(tickets)

if __name__ == "__main__":
    logger.add("Log/02_SyntheticDataGeneration_Jirae.log", format="{time} {level} {message}", level="DEBUG", rotation="100 KB",
               compression="zip")
    logger.debug('02_SyntheticDataGeneration_Jira............')
    start_time = time.time()
    number_of_tickets = int(input("Enter the number of tickets to generate: "))
    logger.debug(f'number_of_tickets ={number_of_tickets}')
    output_filename = input("Enter the output CSV filename: ")
    logger.debug(f'output_filename ={output_filename}')
    tickets = generate_tickets(number_of_tickets)
    save_to_csv(output_filename, tickets)
    logger.debug(f"Generated {number_of_tickets} tickets and saved to {output_filename}")
    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.debug(f'01_SyntheticDataGeneration_Confluence elapsed_time = {elapsed_time} sec')