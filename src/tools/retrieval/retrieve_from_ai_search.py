from promptflow.core import tool
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from promptflow.connections import CognitiveSearchConnection


@tool
def retrieve_from_ai_search(
    query: str,
    index_name: str,
    azure_ai_search_connection: CognitiveSearchConnection
) -> str:
    if not query or not index_name:
        return []

    search_client = SearchClient(
        azure_ai_search_connection.api_base,
        index_name,
        AzureKeyCredential(azure_ai_search_connection.api_key)
    )

    results = search_client.search(
        search_text=query,
        include_total_count=True,
        search_fields=["content"],
        select=["content", "url"],
    )

    retrieved_docs = []
    for result in results:
        retrieved_docs.append({
            "content": result.get("content", ""),
            "source": result.get("url", ""),
        })

    return retrieved_docs
