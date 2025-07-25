"""
Recruiter Agent

This agent reviews the applicant's resume for quality and provides suggestions for improvement.
"""
from ......shared_data import env_variables
from google.adk.agents.llm_agent import LlmAgent
from . import prompt
from .tools import count_characters, exit_loop

# Define the Recruiter Agent
recruiter_agent = LlmAgent(
                name="recruiter_agent",
                model=env_variables.GOOGLE_MODEL,
                instruction=prompt.RECRUITER_PROMPT,
                description="Agent that acts like a recruiter. Reviews resume quality and provides feedback on what to improve or exits the loop if requirements are met",
                output_key="recruiter_feedback",
                tools=[count_characters, exit_loop],
            )


