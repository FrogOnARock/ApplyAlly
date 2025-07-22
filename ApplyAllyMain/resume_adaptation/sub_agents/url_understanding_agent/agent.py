import warnings

from google.adk.agents.llm_agent import Agent

from ...shared_data import env_variables
from . import prompt
from pydantic import BaseModel, Field
warnings.filterwarnings("ignore", category=UserWarning)

class URLOutput(BaseModel):
    LinkedinURL: str = Field(description="The LinkedIn URL provided by the user.")

url_understanding_agent = Agent(
        model=env_variables.GOOGLE_MODEL,
        name="url_understanding_agent",
        description="Your role is to extract the URL from the message history with the user.",
        instruction=prompt.URL_AGENT_PROMPT,
        output_schema=URLOutput,
        output_key="job_description_url"
    )



