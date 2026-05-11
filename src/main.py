from utils import *

from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.skills import Skills, LocalSkills
from agno.team import Team, TeamMode
from agno.db.sqlite import SqliteDb
from agno.memory import MemoryManager

from uiautomator import UiAutomatorTools
from dotenv import load_dotenv
from uuid import uuid4

import os

load_dotenv()
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")

model = Ollama(id="gemma4:31b-cloud", api_key=OLLAMA_API_KEY)

session_id = str(uuid4())
john_doe_id = "john_doe@example.com"


db_file = "db/agent_memory.db"
db = SqliteDb(db_file=db_file, session_table="team_sessions", memory_table="team_memories")

memory_manager = MemoryManager(model=model, db=db)


planner_role = (
    "You are a planner agent that creates a plan to achieve the user's goal. "
    "You will create a step-by-step plan to achieve the user's goal. "
    "You will use the skills available to you to create the plan. "
    "You will not execute any actions, only create a plan.",
)

planner = Agent(
    name="Planner",
    role=planner_role,
    model=model,
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
    model=model,
    tools=[UiAutomatorTools(get_android_device_serial())],
    skills=Skills(loaders=[LocalSkills(str("skills"))]),
    instructions=fetch_file("EXECUTOR_INSTRUCTIONS.md"),
    add_datetime_to_context=True,
    stream=True,
)

automation_team = Team(
    name="Automation Team",
    model=model,
    members=[planner, executor],
    db=db,
    memory_manager=memory_manager,
    update_memory_on_run=True,
    add_memories_to_context=True,
    mode=TeamMode.tasks,
    instructions="You are a team of agents that work together to achieve the user's goal. "
    "The planner agent creates a plan to achieve the user's goal, and the executor agent executes the plan. "
    "You will work together to achieve the user's goal. "
    "You will communicate with each other to achieve the user's goal. ",
)


test_instructions_raw = fetch_json("test_instructions.json")

test_instructions_formatted = prepare_json_to_prompt(test_instructions_raw)

automation_team.print_response(
    test_instructions_formatted, 
    session_id=session_id, 
    user_id=john_doe_id, 
    stream=True
)
