import traceback

from ..rag.get_relevant_procedures_string import get_relevant_procedures_string
from ..utils.get_user_info_string import get_user_info_string


def generate_system_message(cosmo):
    """
    Dynamically generate a system message.

    Takes a cosmo instance,
    returns a string.

    This is easy to replace!
    Just swap out `cosmo.generate_system_message` with another function.
    """

    #### Start with the static system message

    system_message = cosmo.system_message

    #### Add dynamic components, like the user's OS, username, relevant procedures, etc

    system_message += "\n" + get_user_info_string()

    if not cosmo.local:
        try:
            system_message += "\n" + get_relevant_procedures_string(
                cosmo.messages
            )
        except:
            if cosmo.debug_mode:
                print(traceback.format_exc())
            # It's okay if they can't. This just fixes some common mistakes it makes.

    return system_message
