import warnings


from google.adk.tools import ToolContext
from openai import OpenAI
from google.adk.agents.llm_agent import Agent

from ...shared_data import env_variables
from . import prompt


warnings.filterwarnings("ignore", category=UserWarning)



resume_reading_agent = Agent(
        model=env_variables.GOOGLE_MODEL,
        name="resume_reading_agent",
        description="You are the resume reading agent, you will read the content of a PDF."
                    "From this content you will pull the applicants information and store it in session state.",
        instruction=prompt.RESUME_READING_PROMPT,
        output_key="raw_resume_text"
    )



