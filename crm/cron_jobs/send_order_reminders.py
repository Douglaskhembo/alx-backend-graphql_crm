import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# GraphQL client setup
transport = RequestsHTTPTransport(
    url='http://localhost:8000/graphql',
    verify=False,
    retries=3,
)

client = Client(transport=transport, fetch_schema_from_transport=True)

# Define the GraphQL query
query = gql("""
query {
  allOrders {
    id
    orderDate
    customer {
      email
    }
  }
}
""")

# Execute the query
try:
    result = client.execute(query)
    orders = result.get("allOrders", [])

    now = datetime.datetime.now()
    one_week_ago = now - datetime.timedelta(days=7)

    with open("/tmp/order_reminders_log.txt", "a") as log_file:
        for order in orders:
            order_date = datetime.datetime.fromisoformat(order["orderDate"])
            if order_date >= one_week_ago:
                log_file.write(
                    f"{now.strftime('%Y-%m-%d %H:%M:%S')} - Order ID: {order['id']}, Email: {order['customer']['email']}\n"
                )

    print("Order reminders processed!")

except Exception as e:
    print(f"Failed to send order reminders: {str(e)}")
