from celery import shared_task
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime

@shared_task
def generate_crm_report():
    try:
        transport = RequestsHTTPTransport(
            url='http://localhost:8000/graphql',
            verify=False,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=False)

        query = gql("""
        query {
            allCustomers {
                id
            }
            allOrders {
                id
                totalAmount
            }
        }
        """)

        result = client.execute(query)

        num_customers = len(result.get('allCustomers', []))
        orders = result.get('allOrders', [])
        num_orders = len(orders)
        total_revenue = sum(float(order['totalAmount']) for order in orders)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"{timestamp} - Report: {num_customers} customers, {num_orders} orders, {total_revenue:.2f} revenue"

        with open("/tmp/crmreportlog.txt", "a") as log_file:
            log_file.write(log_line + "\n")

    except Exception as e:
        with open("/tmp/crmreportlog.txt", "a") as log_file:
            log_file.write(f"{datetime.now()} - Error: {str(e)}\n")
