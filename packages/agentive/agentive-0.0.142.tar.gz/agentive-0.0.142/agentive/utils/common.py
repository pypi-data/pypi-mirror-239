from tenacity import before_sleep_log,  retry_if_exception_type, stop_after_attempt, wait_exponential
from typing import Any, Dict
import logging
import openai


def common_retry_settings(max_retries: int, verbose: bool = False) -> Dict[str, Any]:

    logger = logging.getLogger(__name__)

    retry_conditions = (
            retry_if_exception_type(openai.error.Timeout) |
            retry_if_exception_type(openai.error.APIError) |
            retry_if_exception_type(openai.error.APIConnectionError) |
            retry_if_exception_type(openai.error.RateLimitError) |
            retry_if_exception_type(openai.error.ServiceUnavailableError)
    )
    return {
        "reraise": True,
        "stop": stop_after_attempt(max_retries),
        "wait": wait_exponential(multiplier=1, min=4, max=10),
        "retry": retry_conditions,
        "before_sleep": before_sleep_log(logger, logging.DEBUG) if verbose else None,
    }