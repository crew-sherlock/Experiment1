from promptflow.core import tool
from azure.search.documents import SearchClient
from azure.identity import DefaultAzureCredential
import os
# Retrieve the IDs and secret to use with ServicePrincipalCredentials


class QueryAISearch:

    def __init__(self):
        self.search_service_name = os.getenv("SEARCH_SERVICE_NAME")
        self.service_endpoint = f"https://{self.search_service_name}.search.windows.net"

    def SearchClient(self, index_name):
        credential = DefaultAzureCredential()

        search_client = SearchClient(
            self.service_endpoint,
            index_name,
            credential
        )
        return search_client


@tool
def retrieve_from_ai_search(
    query: str,
    index_name: str,
    n_results: int = 10,

) -> str:
    if not query or not index_name:
        return []

    search_client = QueryAISearch().SearchClient(index_name)

    results = search_client.search(
        search_text=query,
        include_total_count=True,
        search_fields=["content"],
        select=["content", "url"],
        top=n_results
    )

    retrieved_docs = []
    for result in results:
        retrieved_docs.append({
            "content": result.get("content", ""),
            "source": result.get("url", ""),
        })

    return retrieved_docs
