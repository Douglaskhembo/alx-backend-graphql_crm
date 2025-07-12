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