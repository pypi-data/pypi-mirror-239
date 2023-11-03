import os
import sys

from .cli import cli


OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY", None)
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is required.")


def main():
    """entry point, pass user's OPENAI_API_KEY to program"""
    cli(OPENAI_API_KEY)


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        sys.exit()
