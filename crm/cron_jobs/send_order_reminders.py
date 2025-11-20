#!/usr/bin/env python3

import sys
import logging
from datetime import datetime, timedelta
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# GraphQL endpoint
GRAPHQL_URL = "http://localhost:8000/graphql"

# Log file
LOG_FILE = "/tmp/order_reminders_log.txt"

def main():
    # GraphQL transport setup
    transport = RequestsHTTPTransport(
        url=GRAPHQL_URL,
        verify=True,
        retries=3,
    )

    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Calculate date range: last 7 days
    one_week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    # GraphQL query
    query = gql("""
        query GetRecentOrders($startDate: Date!) {
            orders(orderDate_Gte: $startDate) {
                id
                customer {
                    email
                }
            }
        }
    """)

    # Execute query
    result = client.execute(query, variable_values={"startDate": one_week_ago})

    orders = result.get("orders", [])

    # Log each order
    with open(LOG_FILE, "a") as log:
        for order in orders:
            log.write(
                f"{datetime.now()} - Order ID: {order['id']}, Customer Email: {order['customer']['email']}\n"
            )

    print("Order reminders processed!")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        with open("/tmp/order_reminders_log.txt", "a") as log:
            log.write(f"{datetime.now()} - ERROR: {str(e)}\n")
        sys.exit(1)
