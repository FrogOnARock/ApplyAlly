import warnings

from google.adk.agents import LlmAgent
from google.adk.agents.llm_agent import Agent
from google.adk.tools.tool_context import ToolContext
from google.genai import types
from google.adk.events import Event
import re

from ApplyAllyMain.shared_data import env_variables
from ApplyAllyMain.sub_agents.job_extraction_agent import prompt

warnings.filterwarnings("ignore", category=UserWarning)


def job_extraction_agent():
    return Agent(
        model=env_variables.GOOGLE_MODEL,
        name="job_extraction_agent",
        description="You will extract the job role and company from the stored png."
                    "And you will extract 5 relevant qualifications from the stored text description of the job.",
        instruction=prompt.JOB_EXTRACTION_PROMPT
    )



