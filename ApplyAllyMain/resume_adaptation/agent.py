import asyncio
from google.adk.agents import Agent, SequentialAgent
from google.adk.tools.tool_context import ToolContext
from google.adk.agents.callback_context import CallbackContext
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types # For creating message Content/Parts
from dotenv import load_dotenv
from openai.resources.containers.files import Content
from . import prompt
# Assuming shared_data and sub_agents imports are correct
from .shared_data import env_variables
from google.adk.artifacts import InMemoryArtifactService
from .sub_agents.search_agent.agent import search_agent
from .sub_agents.job_extraction_agent.agent import job_extraction_agent
from .sub_agents.url_understanding_agent.agent import url_understanding_agent
from .sub_agents.resume_reading_agent.agent import resume_reading_agent
import os
from google.adk.agents import SequentialAgent, loop_agent
import datetime
from zoneinfo import ZoneInfo
from google.adk.artifacts import InMemoryArtifactService
from google.adk.sessions import InMemorySessionService
from google.adk.tools.agent_tool import AgentTool

from PyPDF2 import PdfReader
import tkinter as tk
import tkinter.filedialog as filedialog
from io import BytesIO

load_dotenv()
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "TRUE"
os.environ["GOOGLE_CLOUD_PROJECT"] = "applyally"
os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"

def set_session(callback_context: CallbackContext):
    callback_context.state["unique_id"] = "user_1"
    callback_context.state["timestamp"] = datetime.datetime.now(
        ZoneInfo("UTC")
    ).isoformat()


root_agent = Agent(
        name="resume_agent", # Give it a new version name
        model=env_variables.GOOGLE_MODEL,
        description="The main coordinator agent. You handle the initial interaction with the user, obtaining relevant information, and passing to specialized sub-agents.",
        instruction=prompt.ROOT_PROMPT,
        sub_agents=[search_agent, job_extraction_agent],
        tools=[AgentTool(url_understanding_agent), AgentTool(resume_reading_agent)],
        before_agent_callback=set_session
)

session_service = InMemorySessionService()
artifact_service = InMemoryArtifactService()

runner = Runner(agent=root_agent,
                app_name="Resume Alteration App",
                session_service=session_service,
                artifact_service=artifact_service
)



