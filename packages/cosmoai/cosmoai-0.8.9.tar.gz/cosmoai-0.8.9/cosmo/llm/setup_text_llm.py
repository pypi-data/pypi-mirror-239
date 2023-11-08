import os
import traceback

import litellm
import tokentrim as tt

from ..utils.display_markdown_message import display_markdown_message


def setup_text_llm(cosmo):
    """
    Takes an Cosmo (which includes a ton of LLM settings),
    returns a text LLM (an OpenAI-compatible chat LLM with baked-in settings. Only takes `messages`).
    """

    # Pass remaining parameters to LiteLLM
    def base_llm(messages):
        """
        Returns a generator
        """

        system_message = messages[0]["content"]

        messages = messages[1:]
        if cosmo.context_window and cosmo.max_tokens:
            trim_to_be_this_many_tokens = (
                cosmo.context_window - cosmo.max_tokens - 25
            )  # arbitrary buffer
            messages = tt.trim(
                messages,
                system_message=system_message,
                max_tokens=trim_to_be_this_many_tokens,
            )
        else:
            try:
                messages = tt.trim(
                    messages, system_message=system_message, model=cosmo.model
                )
            except:
                display_markdown_message(
                    """
                **We were unable to determine the context window of this model.** Defaulting to 3000.
                If your model can handle more, run `cosmo --context_window {token limit}` or `cosmo.context_window = {token limit}`.
                Also, please set max_tokens: `cosmo --max_tokens {max tokens per response}` or `cosmo.max_tokens = {max tokens per response}`
                """
                )
                messages = tt.trim(
                    messages, system_message=system_message, max_tokens=3000
                )

        if cosmo.debug_mode:
            print("Passing messages into LLM:", messages)

        # Create LiteLLM generator
        params = {
            "model": cosmo.model,
            "messages": messages,
            "stream": True,
        }

        # Optional inputs
        if cosmo.api_base:
            params["api_base"] = cosmo.api_base
        if cosmo.api_key:
            params["api_key"] = cosmo.api_key
        if cosmo.max_tokens:
            params["max_tokens"] = cosmo.max_tokens
        if cosmo.temperature is not None:
            params["temperature"] = cosmo.temperature
        else:
            params["temperature"] = 0.0

        # These are set directly on LiteLLM
        if cosmo.max_budget:
            litellm.max_budget = cosmo.max_budget
        if cosmo.debug_mode:
            litellm.set_verbose = True

        # Report what we're sending to LiteLLM
        if cosmo.debug_mode:
            print("Sending this to LiteLLM:", params)

        return litellm.completion(**params)

    return base_llm
