from utils import *

from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.skills import Skills, LocalSkills
from agno.team import Team, TeamMode

from uiautomator import UiAutomatorTools
from dotenv import load_dotenv

import os

load_dotenv()
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")


planner_role = (
    "You are a planner agent that creates a plan to achieve the user's goal. "
    "You will create a step-by-step plan to achieve the user's goal. "
    "You will use the skills available to you to create the plan. "
    "You will not execute any actions, only create a plan.",
)

planner = Agent(
    name="Planner",
    role=planner_role,
    model=Ollama(id="qwen3.5:cloud", api_key=OLLAMA_API_KEY),
    skills=Skills(loaders=[LocalSkills(str("skills/android-settings-map"))]),
    instructions=fetch_file("PLANNER_INSTRUCTIONS.md"),
    add_datetime_to_context=True,
    stream=True,
)

executor_role = (
    "You are an executor agent that executes the plan created by the planner agent. "
    "You will execute the plan step-by-step to achieve the user's goal. "
    "You will use the skills available to you to execute the plan. "
    "You will not create any plans, only execute the plan created by the planner agent.",
)

executor = Agent(
    name="Executor",
    role=executor_role,
    model=Ollama(id="qwen3.5:cloud", api_key=OLLAMA_API_KEY),
    tools=[UiAutomatorTools(get_android_device_serial())],
    skills=Skills(loaders=[LocalSkills(str("skills"))]),
    instructions=fetch_file("EXECUTOR_INSTRUCTIONS.md"),
    add_datetime_to_context=True,
    stream=True,
)

automation_team = Team(
    name="Automation Team",
    model=Ollama(id="qwen3.5:cloud", api_key=OLLAMA_API_KEY),
    members=[planner, executor],
    mode=TeamMode.tasks,
    instructions="You are a team of agents that work together to achieve the user's goal. " \
    "The planner agent creates a plan to achieve the user's goal, and the executor agent executes the plan. " \
    "You will work together to achieve the user's goal. " \
    "You will communicate with each other to achieve the user's goal. " \
    
)


test_instructions_raw = fetch_json("test_instructions.json")

test_instructions_formatted = prepare_json_to_prompt(test_instructions_raw)

automation_team.print_response(test_instructions_formatted)
