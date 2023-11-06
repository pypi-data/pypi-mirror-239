from typing import List, Union
import logging


def chunk_text(
        text: Union[str, List[Union[str, object]]],
        chunk_size: int,
        overlap: int = 0,
        verbose: bool = False) -> List[Union[str, List[Union[str, object]]]]:
    """
    Chunks a given text or list of tokens into smaller pieces, with optional overlap.

    Parameters:
    - text (str | List[str | object]): The text or list of tokens to be chunked.
    - chunk_size (int): The size of each chunk.
    - overlap (int, optional): The number of overlapping elements between adjacent chunks. Default is 0.
    - verbose (bool, optional): If True, prints log messages for debugging. Default is False.

    Returns:
    List[str] | List[List[str | object]]: A list of chunked text or tokens.

    Raises:
    - ValueError: If the input text is empty.
    - ValueError: If the chunk_size is less than 1.
    - ValueError: If the overlap is negative or greater than or equal to chunk_size.
    """
    if verbose:
        logging.basicConfig(level=logging.DEBUG)

    if not text:
        raise ValueError("The input text cannot be empty.")

    if chunk_size < 1:
        raise ValueError("The chunk size must be greater than 0.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("The overlap must be non-negative and less than the chunk size.")

    if isinstance(text, str):
        text = text.split()

    if verbose:
        logging.debug(f"Input text: {text}")

    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunk = text[i:i + chunk_size]
        if verbose:
            logging.debug(f"Chunk: {chunk}")
        chunks.append(chunk)

    if verbose:
        logging.debug(f"Chunks: {chunks}")

    return chunks

