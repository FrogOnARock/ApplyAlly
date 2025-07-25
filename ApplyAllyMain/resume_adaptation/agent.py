from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.runners import Runner
from dotenv import load_dotenv
from . import prompt
# Assuming shared_data and sub_agents imports are correct
from .shared_data import env_variables
from .sub_agents.sequential_agent_1.agent import sequential_agent_1
from .sub_agents.url_understanding_agent.agent import url_understanding_agent
from .sub_agents.resume_reading_agent.agent import resume_reading_agent
import datetime
from zoneinfo import ZoneInfo
from google.adk.artifacts import InMemoryArtifactService
from google.adk.sessions import InMemorySessionService

from google.adk.tools.agent_tool import AgentTool

import os

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("google_key")


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
        sub_agents=[sequential_agent_1],
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



