import warnings

from google.adk.agents.llm_agent import Agent

from .....shared_data import env_variables
from . import prompt

warnings.filterwarnings("ignore", category=UserWarning)


applicant_agent = Agent(
        model=env_variables.GOOGLE_MODEL,
        name="applicant_agent",
        description="Summarizes the applicant's resume and extract key qualifications.",
        instruction=prompt.APPLICANT_AGENT_PROMPT
    )



