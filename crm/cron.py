import datetime
import requests

def log_crm_heartbeat():
    now = datetime.datetime.now().strftime('%d/%m/%Y-%H:%M:%S')
    message = f"{now} CRM is alive"

    # Optional: Ping GraphQL hello field to ensure endpoint is responsive
    try:
        response = requests.post('http://localhost:8000/graphql', json={"query": "{ __typename }"})
        if response.status_code == 200:
            message += " | GraphQL responsive"
        else:
            message += f" | GraphQL failed: {response.status_code}"
    except Exception as e:
        message += f" | Exception: {str(e)}"

    with open("/tmp/crm_heartbeat_log.txt", "a") as f:
        f.write(message + "\n")