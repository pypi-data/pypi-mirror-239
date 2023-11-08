import traceback

import litellm

from ..code_cosmo.create_code_cosmo import create_code_cosmo
from ..code_cosmo.language_map import language_map
from ..utils.display_markdown_message import display_markdown_message
from ..utils.merge_deltas import merge_deltas
from ..utils.truncate_output import truncate_output


def respond(cosmo):
    """
    Yields tokens, but also adds them to cosmo.messages. TBH probably would be good to seperate those two responsibilities someday soon
    Responds until it decides not to run any more code or say anything else.
    """

    while True:
        system_message = cosmo.generate_system_message()

        # Create message object
        system_message = {"role": "system", "message": system_message}

        # Create the version of messages that we'll send to the LLM
        messages_for_llm = cosmo.messages.copy()
        messages_for_llm = [system_message] + messages_for_llm

        # It's best to explicitly tell these LLMs when they don't get an output
        for message in messages_for_llm:
            if "output" in message and message["output"] == "":
                message["output"] = "No output"

        ### RUN THE LLM ###

        # Add a new message from the assistant to cosmo's "messages" attribute
        # (This doesn't go to the LLM. We fill this up w/ the LLM's response)
        cosmo.messages.append({"role": "assistant"})

        # Start putting chunks into the new message
        # + yielding chunks to the user
        try:
            # Track the type of chunk that the coding LLM is emitting
            chunk_type = None

            for chunk in cosmo._llm(messages_for_llm):
                # Add chunk to the last message
                cosmo.messages[-1] = merge_deltas(cosmo.messages[-1], chunk)

                # This is a coding llm
                # It will yield dict with either a message, language, or code (or language AND code)

                # We also want to track which it's sending to we can send useful flags.
                # (otherwise pretty much everyone needs to implement this)
                if "message" in chunk and chunk_type != "message":
                    chunk_type = "message"
                    yield {"start_of_message": True}
                elif "language" in chunk and chunk_type != "code":
                    chunk_type = "code"
                    yield {"start_of_code": True}
                if "code" in chunk and chunk_type != "code":
                    # (This shouldn't happen though — ^ "language" should be emitted first, but sometimes GPT-3.5 forgets this)
                    # (But I'm pretty sure we handle that? If it forgets we emit Python anyway?)
                    chunk_type = "code"
                    yield {"start_of_code": True}
                elif "message" not in chunk and chunk_type == "message":
                    chunk_type = None
                    yield {"end_of_message": True}

                yield chunk

            # We don't trigger the end_of_message or end_of_code flag if we actually end on either
            if chunk_type == "message":
                yield {"end_of_message": True}
            elif chunk_type == "code":
                yield {"end_of_code": True}

        except litellm.exceptions.BudgetExceededError:
            display_markdown_message(
                f"""> Max budget exceeded

                **Session spend:** ${litellm._current_cost}
                **Max budget:** ${cosmo.max_budget}

                Press CTRL-C then run `cosmo --max_budget [higher USD amount]` to proceed.
            """
            )
            break
        # Provide extra information on how to change API keys, if we encounter that error
        # (Many people writing GitHub issues were struggling with this)
        except Exception as e:
            if (
                cosmo.local == False
                and "auth" in str(e).lower()
                or "api key" in str(e).lower()
            ):
                output = traceback.format_exc()
                raise Exception(
                    f"{output}\n\nThere might be an issue with your API key(s).\n\nTo reset your API key (we'll use OPENAI_API_KEY for this example, but you may need to reset your ANTHROPIC_API_KEY, HUGGINGFACE_API_KEY, etc):\n        Mac/Linux: 'export OPENAI_API_KEY=your-key-here',\n        Windows: 'setx OPENAI_API_KEY your-key-here' then restart terminal.\n\n"
                )
            elif cosmo.local:
                raise Exception(
                    str(e)
                    + """

Please make sure LM Studio's local server is running by following the steps above.

If LM Studio's local server is running, please try a language model with a different architecture.

                    """
                )
            else:
                raise

        ### RUN CODE (if it's there) ###

        if "code" in cosmo.messages[-1]:
            if cosmo.debug_mode:
                print("Running code:", cosmo.messages[-1])

            try:
                # What code do you want to run?
                code = cosmo.messages[-1]["code"]

                # Fix a common error where the LLM thinks it's in a Jupyter notebook
                if cosmo.messages[-1]["language"] == "python" and code.startswith(
                    "!"
                ):
                    code = code[1:]
                    cosmo.messages[-1]["code"] = code
                    cosmo.messages[-1]["language"] = "shell"

                # Get a code cosmo to run it
                language = cosmo.messages[-1]["language"]
                if language in language_map:
                    if language not in cosmo._code_cosmos:
                        cosmo._code_cosmos[
                            language
                        ] = create_code_cosmo(language)
                    code_cosmo = cosmo._code_cosmos[language]
                else:
                    # This still prints the code but don't allow code to run. Let's Cosmo know through output message
                    error_output = f"Error: Cosmo does not currently support {language}."
                    print(error_output)

                    cosmo.messages[-1]["output"] = ""
                    output = "\n" + error_output

                    # Truncate output
                    output = truncate_output(output, cosmo.max_output)
                    cosmo.messages[-1]["output"] = output.strip()
                    break

                # Yield a message, such that the user can stop code execution if they want to
                try:
                    yield {"executing": {"code": code, "language": language}}
                except GeneratorExit:
                    # The user might exit here.
                    # We need to tell python what we (the generator) should do if they exit
                    break

                # Yield each line, also append it to last messages' output
                cosmo.messages[-1]["output"] = ""
                for line in code_cosmo.run(code):
                    yield line
                    if "output" in line:
                        output = cosmo.messages[-1]["output"]
                        output += "\n" + line["output"]

                        # Truncate output
                        output = truncate_output(output, cosmo.max_output)

                        cosmo.messages[-1]["output"] = output.strip()

            except:
                output = traceback.format_exc()
                yield {"output": output.strip()}
                cosmo.messages[-1]["output"] = output.strip()

            yield {"end_of_execution": True}

        else:
            # Doesn't want to run code. We're done
            break

    return
