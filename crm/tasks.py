from celery import shared_task
from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

LOG_FILE = "/tmp/crm_report_log.txt"
GRAPHQL_URL = "http://localhost:8000/graphql"

@shared_task
def generate_crm_report():
    """
    Generates a weekly CRM report: total customers, total orders, total revenue.
    Logs the report to /tmp/crm_report_log.txt with a timestamp.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # GraphQL client
    transport = RequestsHTTPTransport(url=GRAPHQL_URL, verify=True, retries=3)
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # GraphQL query
    query = gql("""
        query {
            totalCustomers
            totalOrders
            totalRevenue
        }
    """)

    try:
        result = client.execute(query)
        customers = result.get("totalCustomers", 0)
        orders = result.get("totalOrders", 0)
        revenue = result.get("totalRevenue", 0.0)

        log_line = f"{timestamp} - Report: {customers} customers, {orders} orders, {revenue} revenue"

        with open(LOG_FILE, "a") as f:
            f.write(log_line + "\n")

        print(log_line)

    except Exception as e:
        with open(LOG_FILE, "a") as f:
            f.write(f"{timestamp} - ERROR: {str(e)}\n")
        print(f"{timestamp} - ERROR: {str(e)}")
