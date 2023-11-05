# store previous generated commands (locally) if executed/copied (don't if aborted)

def save_to_library(nl_input: str, unix_command: str):
    """save to library"""
    return nl_input, unix_command