import requests
import datetime

# Define the GraphQL query
query = """
query {
  allOrders {
    id
    orderDate
    customer {
      email
    }
  }
}
"""

# Send the request to the local GraphQL endpoint
response = requests.post(
    "http://localhost:8000/graphql",
    json={'query': query},
    headers={'Content-Type': 'application/json'}
)

# Parse the results
if response.status_code == 200:
    data = response.json()
    orders = data["data"]["allOrders"]
    now = datetime.datetime.now()
    one_week_ago = now - datetime.timedelta(days=7)

    with open("/tmp/order_reminders_log.txt", "a") as log_file:
        for order in orders:
            order_date = datetime.datetime.fromisoformat(order["orderDate"])
            if order_date >= one_week_ago:
                log_file.write(f"{now} - Order ID: {order['id']} - Email: {order['customer']['email']}\n")

    print("Order reminders processed!")
else:
    print(f"Failed to fetch orders: {response.status_code}")
