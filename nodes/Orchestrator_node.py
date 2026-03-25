from azure.search.documents.indexes import SearchIndexClient
from azure.core.credentials import AzureKeyCredential
import os

SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
INDEX_NAME = "policies-index"


def index_exists():

    client = SearchIndexClient(
        endpoint=SEARCH_ENDPOINT,
        credential=AzureKeyCredential(SEARCH_KEY)
    )

    indexes = [idx.name for idx in client.list_indexes()]

    return INDEX_NAME in indexes


def orchestrator_node(state):

    print("\nOrchestrator: Checking index...")

    if index_exists():
        print("Index exists → skipping indexing")
        return {"index_ready": True}

    print("Index NOT found → need to create")
    return {"index_ready": False}
