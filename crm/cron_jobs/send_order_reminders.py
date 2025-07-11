import requests
from datetime import datetime, timedelta

since = (datetime.now() - timedelta(days=7)).isoformat()

query = """
query {
  orders {
    id
    orderDate
    customer {
      email
    }
  }
}
"""

response = requests.post("http://localhost:8000/graphql", json={"query": query})
data = response.json().get("data", {}).get("orders", [])

with open("/tmp/order_reminders_log.txt", "a") as log:
    for order in data:
        order_date = order["orderDate"]
        if order_date >= since:
            log.write(f"{datetime.now()} - Order {order['id']} → {order['customer']['email']}\n")

print("Order reminders processed!")