from enum import Enum
import subprocess
import sys
import logging
from abc import abstractmethod
from typing import List

if __name__ == "__main__":
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "openai"]
    )

from openai import AzureOpenAI, OpenAIError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmbeddingStrategy(Enum):
    AOAI = "AOAI"


class EmbeddingModel:
    @abstractmethod
    def generate_embedding(self, chunk: str) -> List[float]:
        pass

    @staticmethod
    def get_by_strategy(strategy: EmbeddingStrategy, **kwargs):
        if strategy == EmbeddingStrategy.AOAI:
            return AOAIEmbeddingModel(**kwargs)
        else:
            raise ValueError(f"Invalid strategy: {strategy}")


class AOAIEmbeddingModel(EmbeddingModel):
    def __init__(
        self,
        deployment_name: str,
        azure_endpoint: str,
        api_key: str,
        api_version: str,
        dimension: int = 1536,
    ) -> None:
        self.dimension = dimension
        self.deployment_name = deployment_name
        self._client = AzureOpenAI(
            azure_endpoint=azure_endpoint,
            api_key=api_key,
            api_version=api_version,
        )

    def generate_embedding(self, chunk: str):
        try:
            response = self._client.embeddings.create(
                input=chunk, model=self.deployment_name
            )
            embedding = response.data[0].embedding
            return embedding
        except OpenAIError as e:
            logger.error(f"Failed to generate embedding: {e}")
            return None
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            return None
