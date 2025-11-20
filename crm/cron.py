from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

LOG_FILE = "/tmp/crm_heartbeat_log.txt"
GRAPHQL_URL = "http://localhost:8000/graphql"

def log_crm_heartbeat():
    """
    Logs a heartbeat message every 5 minutes to confirm CRM is alive.
    Optionally queries the GraphQL 'hello' field to verify endpoint responsiveness.
    """
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive"

    # Set up GraphQL client
    transport = RequestsHTTPTransport(
        url=GRAPHQL_URL,
        verify=True,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # GraphQL hello query
    query = gql("""
        query {
            hello
        }
    """)

    try:
        result = client.execute(query)
        if "hello" in result:
            message += " | GraphQL OK"
        else:
            message += " | GraphQL ERROR: no hello field"

    except Exception as e:
        message += f" | GraphQL FAILED: {str(e)}"

    # Append message to log file
    with open(LOG_FILE, "a") as f:
        f.write(message + "\n")

    print(message)  # Useful for testing manually
