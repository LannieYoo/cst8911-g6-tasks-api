import os

from azure.cosmos import CosmosClient
from azure.identity import DefaultAzureCredential

# Connection settings come from the Function App environment variables.
# There is no key or connection string. The Function App uses its
# System-Assigned Managed Identity to talk to Cosmos DB.
COSMOS_ENDPOINT = os.environ["COSMOS_ENDPOINT"]
COSMOS_DATABASE = os.environ.get("COSMOS_DATABASE", "appdb")
COSMOS_CONTAINER = os.environ.get("COSMOS_CONTAINER", "tasks")

_client = None


def get_container():
    """Return the Cosmos DB container client for the tasks container."""
    global _client
    if _client is None:
        _client = CosmosClient(COSMOS_ENDPOINT, credential=DefaultAzureCredential())
    database = _client.get_database_client(COSMOS_DATABASE)
    return database.get_container_client(COSMOS_CONTAINER)
