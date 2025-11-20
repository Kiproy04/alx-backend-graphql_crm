from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

LOG_FILE = "/tmp/crm_heartbeat_log.txt"
LOG_FILE = "/tmp/low_stock_updates_log.txt"
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

def update_low_stock():
    """
    Executes the UpdateLowStockProducts GraphQL mutation every 12 hours.
    Logs updated product names and new stock levels.
    """
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

    # Set up GraphQL client
    transport = RequestsHTTPTransport(
        url=GRAPHQL_URL,
        verify=True,
        retries=3
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # GraphQL mutation
    mutation = gql("""
        mutation {
            updateLowStockProducts {
                updatedProducts {
                    name
                    stock
                }
                message
            }
        }
    """)

    try:
        result = client.execute(mutation)
        updated_products = result["updateLowStockProducts"]["updatedProducts"]
        message_lines = [f"{timestamp} | Updated product: {p['name']}, new stock: {p['stock']}" for p in updated_products]

        # Write to log
        with open(LOG_FILE, "a") as f:
            for line in message_lines:
                f.write(line + "\n")

        if updated_products:
            print(f"{timestamp} | {len(updated_products)} products restocked.")
        else:
            print(f"{timestamp} | No products needed restocking.")

    except Exception as e:
        with open(LOG_FILE, "a") as f:
            f.write(f"{timestamp} | ERROR: {str(e)}\n")
        print(f"{timestamp} | ERROR: {str(e)}")