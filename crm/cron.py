import requests
from datetime import datetime

LOG_FILE = "/tmp/crm_heartbeat_log.txt"
GRAPHQL_URL = "http://localhost:8000/graphql"

def log_crm_heartbeat():
    """
    Writes a heartbeat log every 5 minutes.
    Also optionally checks GraphQL 'hello' field for responsiveness.
    """

    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive"

    # OPTIONAL: Check GraphQL hello field
    try:
        query = {"query": "{ hello }"}
        response = requests.post(GRAPHQL_URL, json=query, timeout=5)

        if response.status_code == 200:
            message += " | GraphQL OK"
        else:
            message += f" | GraphQL ERROR {response.status_code}"

    except Exception as e:
        message += f" | GraphQL FAILED: {str(e)}"

    # Append to log file (never overwrite)
    with open(LOG_FILE, "a") as f:
        f.write(message + "\n")

    print(message)  # Useful for debugging crontab manually
