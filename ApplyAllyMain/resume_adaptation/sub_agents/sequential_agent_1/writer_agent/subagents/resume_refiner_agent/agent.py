"""
LinkedIn Resume Refiner Agent

This agent refines the resume based on feedback to improve quality.
"""
from ......shared_data import env_variables
from google.adk.agents.llm_agent import LlmAgent
from . import prompt


# Define the Resume Refiner Agent
resume_refiner_agent = LlmAgent(
        name="resume_refiner_agent",
        model=env_variables.GOOGLE_MODEL,
        instruction=prompt.RESUME_REFINER_PROMPT,
        description="Refines resume based on feedback to improve quality",
        output_key="current_resume",
        
    )


