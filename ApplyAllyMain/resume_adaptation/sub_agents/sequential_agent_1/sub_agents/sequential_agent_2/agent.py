import warnings

from google.adk.agents import SequentialAgent
from .sub_agents.applicant_agent.agent import applicant_agent
warnings.filterwarnings("ignore", category=UserWarning)


sequential_agent_2 = SequentialAgent(
    name='sequential_agent_2',
    description='You will run the sequential stream to retrieve the applicants information',
    sub_agents=[applicant_agent],
)




