"""
LinkedIn Post Generator Agent

This agent generates the initial LinkedIn post before refinement.
"""
from .....shared_data import env_variables
from google.adk.agents.llm_agent import LlmAgent
from . import prompt

# Define the Resume Generator Agent
resume_generator_agent = LlmAgent(
    name="ResumeGenerator",
    model=env_variables.GOOGLE_MODEL,
    instruction=prompt.RESUME_WRITER_PROMPT,
    description="Generates the initial applicant resume to start the refinement process",
    output_key="current_resume",
)


