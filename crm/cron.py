from datetime import datetime
import requests

def log_crm_heartbeat():
    now = datetime.now().strftime('%d/%m/%Y-%H:%M:%S')
    with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
        f.write(f"{now} CRM is alive\n")
    try:
        r = requests.post("http://localhost:8000/graphql", json={"query": "{ hello }"})
        print("Heartbeat OK" if r.status_code == 200 else "Failed")
    except Exception as e:
        print("Heartbeat Error:", e)
        
def update_low_stock():
    mutation = """
    mutation {
        updateLowStockProducts {
            updatedProducts {
                name
                stock
            }
            message
        }
    }
    """
    try:
        r = requests.post("http://localhost:8000/graphql", json={"query": mutation})
        res = r.json()["data"]["updateLowStockProducts"]["updatedProducts"]
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open("/tmp/low_stock_updates_log.txt", "a") as f:
            for p in res:
                f.write(f"{now} - {p['name']} restocked to {p['stock']}\n")
    except Exception as e:
        print("Stock update error:", e)
