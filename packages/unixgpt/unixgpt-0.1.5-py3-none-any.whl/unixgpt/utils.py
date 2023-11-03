import subprocess
import pyperclip

def execute_unix_command(unix_command: str) -> dict:
    """execute a specific unix command using subprocess"""
    try:
        subprocess.run(unix_command, shell=True, check=True)
        return {"success": f"Command '{unix_command}' ran successfully."}
    except subprocess.SubprocessError:
        return {"error": f"Command '{unix_command}' failed to run."}


def copy_command_to_clipboard(unix_command: str) -> dict:
    """copy a specific command string to a user's clipboard"""
    try:
        pyperclip.copy(unix_command)
        return {"success": f"Command '{unix_command}' copied to clipboard successfully."}
    except pyperclip.PyperclipException:
        return {"error": f"Command '{unix_command}' was not able to be copied."} 
