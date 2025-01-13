import random
from datetime import datetime, timedelta
import json
from faker import Faker

# Initialize Faker
fake = Faker()

# Define templates for different types of Jira tickets
templates = [
    "Bug: The {component} component is not working as expected. Steps to reproduce: {steps}. Expected result: {expected}. Actual result: {actual}.",
    "Feature: Add a new {feature} to the {component} component. This feature should allow users to {action}.",
    "Task: Refactor the {component} component to improve {aspect}. This should include {details}.",
    "Incident: The {component} component is causing a critical issue in production. Impact: {impact}. Steps to mitigate: {mitigation}.",
]

# Define random data for placeholders
components = ["authentication", "payment", "user profile", "dashboard"]
steps = ["log in", "navigate to the dashboard", "click on the profile icon", "submit the form"]
expected_results = ["user is logged in", "dashboard is displayed", "profile page is shown", "form is submitted successfully"]
actual_results = ["error message is shown", "page is not loading", "profile page is blank", "form submission fails"]
features = ["dark mode", "two-factor authentication", "export to CSV", "real-time notifications"]
actions = ["enable dark mode", "set up two-factor authentication", "export data to CSV", "receive notifications in real-time"]
aspects = ["performance", "readability", "maintainability", "security"]
details = ["code cleanup", "adding comments", "removing unused variables", "updating dependencies"]
impacts = ["users cannot log in", "payments are failing", "profile data is not loading", "dashboard is not updating"]
mitigations = ["rollback the deployment", "restart the server", "apply a hotfix", "notify the users"]

# Function to generate a random Jira ticket description
def generate_random_description():
    template = random.choice(templates)
    description = template.format(
        component=random.choice(components),
        steps=", ".join(random.sample(steps, 2)),
        expected=random.choice(expected_results),
        actual=random.choice(actual_results),
        feature=random.choice(features),
        action=random.choice(actions),
        aspect=random.choice(aspects),
        details=", ".join(random.sample(details, 2)),
        impact=random.choice(impacts),
        mitigation=random.choice(mitigations)
    )
    return description

# Function to generate a short description
def generate_short_description():
    short_templates = [
        "Bug in {component} component.",
        "New feature: {feature}.",
        "Refactor {component} for better {aspect}.",
        "Critical issue in {component} component."
    ]
    short_template = random.choice(short_templates)
    short_description = short_template.format(
        component=random.choice(components),
        feature=random.choice(features),
        aspect=random.choice(aspects)
    )
    return short_description

def generate_resolution(description):
    resolution_steps = [
        "Restarted the server.",
        "Cleared the cache.",
        "Updated the configuration.",
        "Applied a hotfix.",
        "Rolled back the deployment.",
        "Notified the users.",
        "Performed a code review.",
        "Ran additional tests."
    ]
    additional_steps = ", ".join(random.sample(resolution_steps, 2))
    return f"Resolution steps taken: {description} Additionally, {additional_steps}."

def generate_incident():
    priorities = ["Low", "Medium", "High", "Critical"]
    states = ["New", "In Progress", "Resolved", "Closed"]
    categories = ["IT Services", "Software", "Hardware", "Network"]
    urgency_impact = ["Low", "Medium", "High"]
    
    state = random.choice(states)
    description = generate_random_description()
    resolution = generate_resolution(description) if state in ["In Progress", "Resolved", "Closed"] else None
    
    return {
        "incident_id": f"INC{random.randint(100000, 999999)}",
        "short_description": generate_short_description(),
        "description": description,
        "priority": random.choice(priorities),
        "state": state,
        "created_at": (datetime.now() - timedelta(days=random.randint(1, 100))).isoformat(),
        "updated_at": datetime.now().isoformat(),
        "assigned_to": fake.name(),
        "category": random.choice(categories),
        "impact": random.choice(urgency_impact),
        "urgency": random.choice(urgency_impact),
        "resolution": resolution
    }

def generate_jira_story():
    types = ["Bug", "Feature", "Task", "Epic"]
    statuses = ["To Do", "In Progress", "Done", "Closed"]
    priorities = ["Low", "Medium", "High", "Critical"]
    
    return {
        "story_id": f"STORY-{random.randint(1000, 9999)}",
        "summary": generate_short_description(),
        "description": generate_random_description(),
        "type": random.choice(types),
        "status": random.choice(statuses),
        "created_at": (datetime.now() - timedelta(days=random.randint(1, 100))).isoformat(),
        "updated_at": datetime.now().isoformat(),
        "reporter": fake.name(),
        "assignee": fake.name(),
        "priority": random.choice(priorities),
        "labels": [random.choice(["API", "UI", "Backend", "Database"])]
    }

# Generate Data
mock_ied_data =  [generate_incident() for _ in range(4000)]

# Generate Data
mock_jira_data =  [generate_jira_story() for _ in range(5000)]

# Save to JSON
with open("../../../mongo_dump/mock_ied_data.json", "w") as file:
    json.dump(mock_ied_data, file, indent=4)

with open("../../../mongo_dump/mock_jira_data.json", "w") as file:
    json.dump(mock_jira_data, file, indent=4)    