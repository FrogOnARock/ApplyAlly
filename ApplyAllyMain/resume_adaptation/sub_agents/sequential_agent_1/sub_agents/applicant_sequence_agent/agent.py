import warnings

from google.adk.agents import SequentialAgent
from .sub_agents.applicant_agent.agent import applicant_agent
warnings.filterwarnings("ignore", category=UserWarning)


applicant_sequence_agent = SequentialAgent(
    name="applicant_sequence_agent",
    description='You will run the sequential stream to retrieve the applicants information',
    sub_agents=[applicant_agent],
)




