import logging
from typing import List, Dict

from promptflow.core import tool
import asyncio

from src.tools.sql.query_sql import QuerySql

logger = logging.getLogger(__name__)

# Please notice, this is not user safe query, if a user uses this method,
# they can inject malicious code.


@tool
def retrieve_sql_data(
    query: str, params: List[str]
) -> Dict:
    if not query:
        return {"status": "error", "message": "Please provide a SQL query"}
    try:
        sql = QuerySql()
        df = asyncio.run(sql.execute(query, params))
        text = df.to_dict()
        return {"status": "success", "data": text}
    except Exception as e:
        logger.error("failed to retrieve SQL data", exc_info=True)
        return {"status": "error", "message": f"Failed to execute query with error {e}"}
