from __future__ import annotations
import uuid

import pandas as pd

from typing import Dict, Any, List, Optional

from agentive.embeddings import Embeddings
from agentive.utils.evaluation.distance import cosine_similarity


class LocalVectorStorage:
    """Local vector storage based on pandas/numpy.

    Attributes:
        embed_model (Embeddings): The embedding model to use.
        storage (pd.DataFrame): DataFrame for storing vectors.
    """

    def __init__(self, embed_model: Embeddings):
        """Initialize LocalVectorStorage.

        Args:
            embed_model (Embeddings): The embedding model to use.
        """
        self.embed_model = embed_model
        self.storage = pd.DataFrame()

    def add(self, content: str, **kwargs: Any) -> None:
        """Add a message to the storage.

        Args:
            content (str): The content to be stored.
            **kwargs (Any): Additional keyword arguments.
        """
        self.add_many([{'content': content, **kwargs}])

    def add_many(self, entries: List[Dict[str, Any]]) -> None:
        """Add many entries to the storage.

        Args:
            entries (List[Dict[str, Any]]): The entries to be stored.
        """
        # Ensure that all entries have a content field
        try:
            assert all('content' in entry for entry in entries)
        except AssertionError:
            raise ValueError("All entries must have a content field.")

        contents = [entry['content'] for entry in entries]
        bulk_embeddings = self.embed_model.embed_bulk(texts=contents)

        row_data = []
        for idx, entry in enumerate(entries):
            prepared_data = self._prepare_row_data(**entry)
            prepared_data['embedding'] = bulk_embeddings[idx]

            row_data.append(prepared_data)

        self.storage = pd.concat([self.storage, pd.DataFrame(row_data)], ignore_index=True)

    def update(self, _id: str, **kwargs: Any) -> None:
        """Update a message in the storage.

        Args:
            _id (str): The ID of the message to update.
            **kwargs (Any): Additional keyword arguments.
        """
        matched_indices = self.storage.index[self.storage['id'] == _id]
        if not matched_indices.empty:
            idx = matched_indices[0]
            row_data = self._prepare_row_data(**kwargs)
            self.storage.loc[idx] = row_data

    def delete(self, _id: str) -> None:
        """Delete a message from the storage.

        Args:
            _id (str): The ID of the message to delete.
        """
        self.storage = self.storage[self.storage['id'] != _id]

    def get(self, _id: str) -> Dict[str, Any]:
        """Get a message from the storage.

        Args:
            _id (str): The ID of the message to retrieve.

        Returns:
            Dict[str, Any]: The message data.
        """
        return self.storage[self.storage['id'] == _id].to_dict(orient='records')[0]

    def get_all(self) -> List[Dict[str, Any]]:
        """Get all messages from the storage.

        Returns:
            List[Dict[str, Any]]: All messages in the storage.
        """
        return self.storage.to_dict(orient='records')

    def search(self, query: str = None, n: int = 5, filters: Optional[Dict[str, Any]] = None, return_score: bool = False) -> List[Dict[str, Any]]:
        """Search for messages in the storage.

        Args:
            query (str): The search query.
            n (int, optional): Number of results to return. Defaults to 5.
            filters (Optional[Dict[str, Any]], optional): Filters to apply. Defaults to None.
            return_score (bool, optional): Whether to return the score for each result. Defaults to False.

        Returns:
            List[Dict[str, Any]]: List of messages matching the search query.
        """
        if self.storage.empty:
            return []

        query_embedding = self.embed_model.embed(query)

        storage = self.storage.copy()

        if query:
            similarities = storage['embedding'].apply(
                lambda x: cosine_similarity(query_embedding, x)
            )

            if return_score:
                storage['score'] = similarities

            top_indices = similarities.nlargest(n).index
            storage = storage.iloc[top_indices]

        if filters:
            for key, value in filters.items():
                assert key in storage.columns, f"Key {key} does not exist in storage."
                storage = storage[storage[key] == value]

        return storage.to_dict(orient='records')

    def clear(self) -> None:
        """Clear all rows from storage."""
        self.storage = pd.DataFrame()

    @staticmethod
    def _prepare_row_data(**kwargs: Any) -> Dict[str, Any]:
        """Prepare a message for storage.

        Args:
            content (str): The text content of the message.
            **kwargs (Any): Additional keyword arguments.

        Returns:
            Dict[str, Any]: The message prepared for storage.
        """
        return {'id': kwargs.get('id', str(uuid.uuid4())), **kwargs}

    def __len__(self) -> int:
        return len(self.storage)