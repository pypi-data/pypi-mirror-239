from colorama import Fore, Style


prompt_types = ["info", "debug", "warn", "success", "fail"]


class GlitchPrompts:
    """
    Create object that houses all the prompts and their colors.
    """

    def __init__(self, **kwargs):
        info_prompt: str = kwargs.get("info_prompt", "[i]")
        debug_prompt: str = kwargs.get("debug_prompt", "[d]")
        warn_prompt: str = kwargs.get("warn_prompt", "[w]")
        success_prompt: str = kwargs.get("success_prompt", "[+]")
        fail_prompt: str = kwargs.get("fail_prompt", "[!]")

        self.color_info = Style.RESET_ALL
        self.color_debug = Fore.YELLOW
        self.color_warn = Fore.YELLOW
        self.color_success = Fore.GREEN
        self.color_fail = Fore.RED

        self.info = f"{self.color_info}{info_prompt}{Style.RESET_ALL}"
        self.debug = f"{self.color_debug}{debug_prompt}{Style.RESET_ALL}"
        self.warn = f"{self.color_warn}{warn_prompt}{Style.RESET_ALL}"
        self.success = f"{self.color_success}{success_prompt}{Style.RESET_ALL}"
        self.fail = f"{self.color_fail}{fail_prompt}{Style.RESET_ALL}"
