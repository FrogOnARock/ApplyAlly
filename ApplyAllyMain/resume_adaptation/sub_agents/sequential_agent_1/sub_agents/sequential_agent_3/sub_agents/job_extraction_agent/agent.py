import warnings

from google.adk.agents.llm_agent import Agent

from .....shared_data import env_variables
from . import prompt

warnings.filterwarnings("ignore", category=UserWarning)


job_extraction_agent = Agent(
        model=env_variables.GOOGLE_MODEL,
        name="job_extraction_agent",
        description="You will extract the job role and company from stored text."
                    "And you will extract 5 relevant qualifications from the stored text description of the job.",
        instruction=prompt.JOB_EXTRACTION_PROMPT
    )



