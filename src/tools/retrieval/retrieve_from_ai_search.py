from promptflow.core import tool
from azure.search.documents import SearchClient
from azure.identity import DefaultAzureCredential
# Retrieve the IDs and secret to use with ServicePrincipalCredentials


@tool
def retrieve_from_ai_search(
    query: str,
    index_name: str,
    service_endpoint: str,
    n_results: int = 10,

) -> str:
    if not query or not index_name:
        return []

    credential = DefaultAzureCredential()

    search_client = SearchClient(
        service_endpoint,
        index_name,
        credential
    )

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
