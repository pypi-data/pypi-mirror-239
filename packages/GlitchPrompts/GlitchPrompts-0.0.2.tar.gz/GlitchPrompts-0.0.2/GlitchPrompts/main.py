from .prompts import GlitchPrompts, prompt_types


gp = GlitchPrompts()


def glitch_print(message: str, prompt: str = "info"):
    """
    Main purpose is to display message using 'info' prompt.
    Use specific prompt upon request.
    :param message: typical message from print statement
    :param prompt: prompt_types
    :return:
    """

    if prompt not in prompt_types:
        raise TypeError(
            "Unrecognized 'prompt' type. Please double check and try again."
        )

    prompted_message = ""
    match prompt:
        case "info":
            prompted_message = f"{gp.info} {message}"
        case "debug":
            prompted_message = f"{gp.debug} {message}"
        case "warn":
            prompted_message = f"{gp.warn} {message}"
        case "fail":
            prompted_message = f"{gp.fail} {message}"
        case "success":
            prompted_message = f"{gp.success} {message}"

    print(prompted_message)


if __name__ == "__main__":
    glitch_print("Success!", prompt="success")
