from typing import Union
import numpy as np


def cosine_similarity(query: Union[list, np.ndarray],
                      target: Union[list, np.ndarray]) -> float:
    """Compute the cosine similarity between two vectors.

    Args:
        query (Union[list, np.ndarray]): The query vector.
        target (Union[list, np.ndarray]): The target vector.

    Returns:
        float: The cosine similarity between the two vectors.
    """

    return np.dot(query, target) / (np.linalg.norm(query) * np.linalg.norm(target))


def euclidean_distance(query: Union[list, np.ndarray],
                       target: Union[list, np.ndarray]) -> float:
    """Compute the Euclidean distance between two vectors.

    Args:
         query (Union[list, np.ndarray]): The query vector.
         target (Union[list, np.ndarray]): The target vector.

    Returns:
        float: The Euclidean distance between the two vectors.
    """
    query, target = map(np.array, (query, target))
    return np.linalg.norm(query - target)


def manhattan_distance(query: Union[list, np.ndarray],
                       target: Union[list, np.ndarray]) -> float:
    """Compute the Manhattan distance between two vectors.

    Args:
        query (Union[list, np.ndarray]): The query vector.
        target (Union[list, np.ndarray]): The target vector.

    Returns:
        float: The Manhattan distance between the two vectors.
    """
    query, target = map(np.array, (query, target))
    return np.sum(np.abs(query - target))

