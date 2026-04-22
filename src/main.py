from utils import *

from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.skills import Skills, LocalSkills

from uiautomator import UiAutomatorTools
from dotenv import load_dotenv

import os

load_dotenv()
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")
agent_instructions = fetch_file("INSTRUCTIONS.md")

agent = Agent(
    model=Ollama(id="qwen3.5:cloud", api_key=OLLAMA_API_KEY),
    tools=[UiAutomatorTools(get_android_device_serial())],
    skills=Skills(loaders=[LocalSkills(str("skills"))]),
    instructions=agent_instructions,
    add_datetime_to_context=True,
    markdown=True,
    stream=True,
)

test_instructions = fetch_json("test_instructions.json")

agent.print_response(test_instructions)
