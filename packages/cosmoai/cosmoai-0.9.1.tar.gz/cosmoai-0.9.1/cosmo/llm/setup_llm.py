import os

import litellm

from .convert_to_coding_llm import convert_to_coding_llm
from .setup_openai_coding_llm import setup_openai_coding_llm
from .setup_text_llm import setup_text_llm


def setup_llm(cosmo):
    """
    Takes a Cosmo (which includes a ton of LLM settings),
    returns a Coding LLM (a generator that streams deltas with `message` and `code`).
    """

    if not cosmo.local and (
        cosmo.model in litellm.open_ai_chat_completion_models
        or cosmo.model.startswith("azure/")
    ):
        # Function-calling LLM
        coding_llm = setup_openai_coding_llm(cosmo)
    else:
        # Non-function-calling LLM
        text_llm = setup_text_llm(cosmo)
        coding_llm = convert_to_coding_llm(text_llm, debug_mode=cosmo.debug_mode)

    return coding_llm
