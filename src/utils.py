import subprocess
from pathlib import Path
import json

def get_android_device_serial():
    """
    Returns the serial number of a connected Android device.
    
    Returns:
        str: The serial number of the device, or None if no device is found.
    """
    try:
        result = subprocess.run(
            ["adb", "devices", "-l"],
            capture_output=True,
            text=True,
            check=True
        )
        
        lines = result.stdout.strip().split('\n')
        if len(lines) > 1:
            # First line is "List of attached devices"
            device_line = lines[1].split()
            if device_line:
                return device_line[0]
    except subprocess.CalledProcessError as e:
        print(f"Error running adb command: {e}")
    except FileNotFoundError:
        print("adb command not found. Ensure Android SDK is installed.")
    
    return None

def fetch_file(file_path: str) -> str:
    instructions_path = Path(__file__).resolve().parent / file_path
    with instructions_path.open("r", encoding="utf-8") as f:
        agent_instructions = f.read()
    return agent_instructions

def fetch_json(file_path: str) -> dict:
    json_path = Path(__file__).resolve().parent / file_path
    with json_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def prepare_json_to_prompt(test_data: dict) -> str:
    """
    Prepares a JSON object to be included in a prompt by converting it to a string.
    
    Args:
        test_data (dict): The test data to prepare.
    """
    user_message = f"""
    {test_data['test_instructions']}

    Setup: {test_data['test_setup']}
    Expected Results: {test_data['expected_results']}
    Comments: {test_data['comments']}
    """
    return user_message