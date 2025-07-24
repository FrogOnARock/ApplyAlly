import warnings

from google.adk.agents import LlmAgent
from google.adk.agents.llm_agent import Agent
from google.adk.tools.tool_context import ToolContext
from google.genai import types
from google.adk.events import Event
import re

from shared_data import env_variables
from sub_agents.applicant_agent import prompt

warnings.filterwarnings("ignore", category=UserWarning)


def job_extraction_agent():
    return Agent(
        model=env_variables.GOOGLE_MODEL,
        name="applicant_agent",
        description="Summarizes the applicant's resume and extract key qualifications.",
        instruction=prompt.APPLICANT_AGENT_PROMPT
    )



