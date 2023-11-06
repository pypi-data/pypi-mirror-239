from typing import Any, Dict, List, Union
import logging


def remove_keys_recursively(d: Dict[Any, Any],
                            keys_to_remove: Union[str, List[str]],
                            verbose: bool = False) -> Dict[Any, Any]:
    """
    Recursively removes specified keys from a dictionary.

    Parameters:
    - d (Dict[Any, Any]): The dictionary from which keys should be removed.
    - keys_to_remove (str | List[str]): The key or list of keys to remove.
    - verbose (bool, optional): If True, prints log messages for debugging. Default is False.

    Returns:
    Dict[Any, Any]: The dictionary with keys removed.

    Raises:
    - ValueError: If the input dictionary is empty.
    - TypeError: If the input is not a dictionary.
    """

    # Initialize logger
    logger = logging.getLogger(__name__)
    if verbose:
        logging.basicConfig(level=logging.DEBUG)

    # Error handling
    if not isinstance(d, dict):
        raise TypeError("Input should be a dictionary.")

    if not d:
        raise ValueError("The input dictionary should not be empty.")

    # Make keys_to_remove a list if it's a single string
    if isinstance(keys_to_remove, str):
        keys_to_remove = [keys_to_remove]

    # Main logic for removing keys
    new_dict = {}
    for k, v in d.items():
        if k not in keys_to_remove:
            if isinstance(v, dict):
                new_dict[k] = remove_keys_recursively(v, keys_to_remove, verbose)
            else:
                new_dict[k] = v

            if verbose:
                logger.debug(f"Kept key: {k}, value: {v}")
        else:
            if verbose:
                logger.debug(f"Removed key: {k}")

    return new_dict