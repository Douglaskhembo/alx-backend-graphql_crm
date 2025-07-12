from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import datetime

def log_crm_heartbeat():
    now = datetime.datetime.now().strftime('%d/%m/%Y-%H:%M:%S')
    message = f"{now} CRM is alive"

    # Setup GraphQL client to call hello field
    try:
        transport = RequestsHTTPTransport(
            url='http://localhost:8000/graphql',
            verify=False,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=False)

        query = gql("""
        query {
            __typename
        }
        """)
        result = client.execute(query)
        message += " | GraphQL responsive"
    except Exception as e:
        message += f" | GraphQL error: {str(e)}"

    with open("/tmp/crm_heartbeat_log.txt", "a") as f:
        f.write(message + "\n")

def update_low_stock():
    try:
        transport = RequestsHTTPTransport(
            url='http://localhost:8000/graphql',
            verify=False,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=False)

        mutation = gql("""
        mutation {
            updateLowStockProducts {
                success
                updatedProducts {
                    name
                    stock
                }
            }
        }
        """)

        result = client.execute(mutation)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_lines = [f"{timestamp} - Updated Products:"]

        for product in result['updateLowStockProducts']['updatedProducts']:
            log_lines.append(f"- {product['name']}: {product['stock']}")

        with open("/tmp/low_stock_updates_log.txt", "a") as f:
            f.write("\n".join(log_lines) + "\n")

    except Exception as e:
        with open("/tmp/low_stock_updates_log.txt", "a") as f:
            f.write(f"{datetime.datetime.now()} - Error: {str(e)}\n")